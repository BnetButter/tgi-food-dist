import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jwt  # PyJWT
import os
from accounts.models import User
from django.utils.timezone import now

AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_CLIENT_SECRET = os.environ["AUTH0_CLIENT_SECRET"]
JWT_SECRET = os.environ["JWT_SECRET"]

@csrf_exempt
def token_exchange(request):
    """
    Exchanges the authorization code for a session token.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    # Parse the incoming request data
    data = request.POST
    code = data.get("code")
    redirect_uri = data.get("redirect_uri")

    if not code or not redirect_uri:
        return JsonResponse({"error": "Missing 'code' or 'redirect_uri'"}, status=400)

    # Auth0 token endpoint URL
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"

    # Request payload for token exchange
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    try:
        # Make the request to Auth0
        response = requests.post(token_url, json=payload)
        response_data = response.json()

        if response.status_code != 200:
            return JsonResponse({"error": "Failed to exchange token", "details": response_data}, status=response.status_code)

        # Extract the ID token
        id_token = response_data.get("id_token")
        if not id_token:
            return JsonResponse({"error": "No ID token in response."}, status=400)

        # Decode the ID token without validation (just to access claims)
        decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
        
        
        user, _ = User.objects.get_or_create(
            id=decoded_id_token["sub"],
            first_name=decoded_id_token.get("given_name"),
            last_name=decoded_id_token.get("family_name"),
            email=decoded_id_token["email"],
        )

        user.last_login = now()
        user.save()
    
        # Re-sign the ID token with your own secret key
        session_token = jwt.encode(
            decoded_id_token, 
            JWT_SECRET, 
            algorithm="HS256"
        )


        response = JsonResponse({"token": session_token})

        # Set the session token in a secure cookie
        response.set_cookie(
            "sessionid",
            session_token,
            httponly=True,             # Prevents JavaScript access to the cookie
            secure=True,               # Ensures the cookie is only sent over HTTPS
            samesite="Lax",            # Mitigates CSRF attacks (can be "Strict" or "None" if needed)
            max_age=3600               # Set cookie expiration in seconds (optional)
        )
        return response
    
    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "ID token has expired."}, status=401)
    except jwt.InvalidTokenError as e:
        return JsonResponse({"error": "Invalid ID token.", "details": str(e)}, status=401)
    except Exception as e:
        return JsonResponse({"error": "An error occurred during token exchange.", "details": str(e)}, status=500)

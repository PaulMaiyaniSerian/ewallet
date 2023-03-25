# ewallet
Prototype with mpesa express stkpush working.. production ready version coming soon

<!-- add .env file in settings.py -->
SECRET_KEY=supersecret
HOST_DOMAIN=yourtunnelip or domain(https)

SHORTCODE=174379
TESTMSISDN=254708374149
CONSUMER_KEY=your mpesa consumer key
CONSUMER_SECRET=your mpesa consumer secret
PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919

MPESA_AUTH_URL=https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials
MPESA_REGISTER_CALLBACK_URL=https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl
PROCESS_STKPUSH_URL=https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest
C2B_SIMULATE_URL=https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate
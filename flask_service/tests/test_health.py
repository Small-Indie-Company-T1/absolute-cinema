from flask import Flask


def create_test_client():
    app = Flask(__name__)

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app.test_client()


def test_healthcheck():
    client = create_test_client()

    response = client.get("/health")

    assert response.status_code == 200
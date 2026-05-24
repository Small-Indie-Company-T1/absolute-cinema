from flask import Flask


def create_test_client():
    app = Flask(__name__)

    @app.route("/reviews")
    def reviews():
        return {"items": []}, 200

    return app.test_client()


def test_moderation_stub():
    client = create_test_client()

    response = client.get("/reviews")

    assert response.status_code == 200
use axum::{routing::get, Router};

async fn get_order() -> &'static str {
    "order"
}

fn routes() -> Router {
    Router::new().route("/release/orders", get(get_order))
}

fn main() {
    let _app = routes();
}

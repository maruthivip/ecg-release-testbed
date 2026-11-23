Rails.application.routes.draw do
  get "/release/orders/:id", to: "orders#show"
end

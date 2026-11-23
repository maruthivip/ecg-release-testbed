package orders

import "net/http"

func GetOrder(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
}

func Routes(mux *http.ServeMux) {
	mux.HandleFunc("/release/orders", GetOrder)
}

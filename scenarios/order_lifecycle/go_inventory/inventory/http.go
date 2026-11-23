package inventory

import (
	"net/http"

	"gorm.io/gorm"
)

func Handler(db *gorm.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		orderID := r.URL.Query().Get("order_id")
		_, err := FindByOrder(r.Context(), db, orderID)
		if err != nil {
			http.Error(w, "reservation unavailable", http.StatusNotFound)
			return
		}
		w.WriteHeader(http.StatusOK)
	}
}

func Routes(mux *http.ServeMux, db *gorm.DB) {
	mux.HandleFunc("/internal/inventory/reservations", Handler(db))
}

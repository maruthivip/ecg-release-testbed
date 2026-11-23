package inventory

import (
	"context"
	"errors"

	"gorm.io/gorm"
)

func Reserve(ctx context.Context, db *gorm.DB, orderID, sku string, quantity int) error {
	if orderID == "" || sku == "" || quantity <= 0 {
		return errors.New("invalid reservation")
	}
	return db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		return tx.Create(&Reservation{OrderID: orderID, SKU: sku, Quantity: quantity}).Error
	})
}

func FindByOrder(ctx context.Context, db *gorm.DB, orderID string) (Reservation, error) {
	var reservation Reservation
	err := db.WithContext(ctx).Where("order_id = ?", orderID).First(&reservation).Error
	return reservation, err
}

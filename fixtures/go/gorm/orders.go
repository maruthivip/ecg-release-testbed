package orders

import "gorm.io/gorm"

type Order struct {
	ID    uint `gorm:"primaryKey"`
	Total int
}

func CreateOrder(db *gorm.DB, order *Order) error {
	return db.Create(order).Error
}

func FindOrder(db *gorm.DB, id uint) (Order, error) {
	var order Order
	result := db.First(&order, id)
	return order, result.Error
}

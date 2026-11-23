package inventory

import "time"

type Reservation struct {
	ID        uint `gorm:"primaryKey"`
	OrderID   string `gorm:"uniqueIndex;not null"`
	SKU       string `gorm:"index;not null"`
	Quantity  int
	CreatedAt time.Time
}

func (Reservation) TableName() string {
	return "inventory_reservations"
}

package orders

import "github.com/gin-gonic/gin"

func GetOrder(c *gin.Context) {
	c.String(200, c.Param("id"))
}

func Routes(router *gin.Engine) {
	router.GET("/release/orders/:id", GetOrder)
}

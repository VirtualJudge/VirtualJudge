package main

import "github.com/kataras/iris/v12"

func main() {
	app := iris.New()

	err := app.Listen(":8080")
	if err != nil {
		return
	}
}

package main

import "github.com/kataras/iris/v12"

func main() {
	app := iris.New()
	api := app.Party("/api")
	{
		v1 := api.Party("/v1")
		{
			v1.PartyFunc("/problem", problemRouter)
		}
	}
	err := app.Run(iris.Addr(":8080"))
	if err != nil {
		return
	}
}

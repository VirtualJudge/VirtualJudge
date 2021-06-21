package main

import "github.com/kataras/iris/v12"

type User struct {
	Firstname    string `json:"firstname"`
	Lastname     string `json:"lastname"`
	IgnoredField int    `json:"-"`
}

func problemRouter(problem iris.Party) {
	problem.Get("/", func(ctx iris.Context) {
		_, err := ctx.HTML("Hello World.")
		if err != nil {
			return
		}
	})
	problem.Get("/{pid: int}", func(ctx iris.Context) {
		response := User{
			Firstname:    "makis",
			Lastname:     "maropoulos",
			IgnoredField: 42,
		}

		_, err := ctx.JSON(response)
		if err != nil {
			return
		}
	})
}

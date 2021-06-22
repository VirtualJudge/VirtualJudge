package interfaces

import "github.com/kataras/iris/v12"

func ProblemRouter(problem iris.Party) {

	problem.Get("/", func(ctx iris.Context) {
		_, err := ctx.HTML("Hello World.")
		if err != nil {
			return
		}
	})
}

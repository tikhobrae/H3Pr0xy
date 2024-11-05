package main

import (
	"github.com/projectdiscovery/gologger"
	"github.com/tikhobrae/H3Pr0xy/tree/main/src/GoScanner/internal/runner"
)

func main() {
	opt := runner.Options()

	if err := runner.New(opt); err != nil {
		gologger.Fatal().Msgf("Error! %s", err)
	}
}

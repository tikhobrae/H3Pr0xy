package main

import (
	"bufio"
	"fmt"
	"log"
	"os/exec"
	"sync"

	"github.com/jroimartin/gocui"
)

func main() {
	g, err := gocui.NewGui(gocui.OutputNormal)
	if err != nil {
		log.Panicln(err)
	}
	defer g.Close()

	g.SetManagerFunc(layout)

	if err := g.SetKeybinding("", gocui.KeyCtrlC, gocui.ModNone, quit); err != nil {
		log.Panicln(err)
	}

	go runScripts(g)

	if err := g.MainLoop(); err != nil && err != gocui.ErrQuit {
		log.Panicln(err)
	}
}

func layout(g *gocui.Gui) error {
	maxX, maxY := g.Size()

	// Left Top
	if v, err := g.SetView("left_top", 0, 0, maxX/2-1, maxY/2-1); err != nil {
		if err != gocui.ErrUnknownView {
			return err
		}
		v.Title = "Left Top"
	}

	// Left Bottom
	if v, err := g.SetView("left_bottom", 0, maxY/2, maxX/2-1, maxY-1); err != nil {
		if err != gocui.ErrUnknownView {
			return err
		}
		v.Title = "Left Bottom"
	}

	// Right
	if v, err := g.SetView("right", maxX/2, 0, maxX-1, maxY-1); err != nil {
		if err != gocui.ErrUnknownView {
			return err
		}
		v.Title = "Right"
	}

	return nil
}

func runScripts(g *gocui.Gui) {
	var wg sync.WaitGroup

	wg.Add(3)
	go runScript(g, "python", "../python/Scrap/NLP.py", "", "left_top", &wg)
	go runScript(g, "go", "run", "api.go", "right", &wg)
	go runScript(g, ".\\mubeng.bat", "", "", "left_bottom", &wg)

	wg.Wait()
}

func runScript(g *gocui.Gui, name string, arg1 string, arg2 string, viewName string, wg *sync.WaitGroup) {
	defer wg.Done()

	cmd := exec.Command(name, arg1, arg2)
	stdout, _ := cmd.StdoutPipe()
	stderr, _ := cmd.StderrPipe()

	if err := cmd.Start(); err != nil {
		log.Panicln(err)
	}

	output := make(chan string)
	var once sync.Once

	go func() {
		scanner := bufio.NewScanner(stdout)
		for scanner.Scan() {
			output <- scanner.Text()
		}
		once.Do(func() { close(output) })
	}()

	go func() {
		scanner := bufio.NewScanner(stderr)
		for scanner.Scan() {
			output <- scanner.Text()
		}
		once.Do(func() { close(output) })
	}()

	go func() {
		for line := range output {
			outputLine(g, viewName, line)
		}
	}()

	cmd.Wait()
}

func outputLine(g *gocui.Gui, viewName string, line string) {
	g.Update(func(g *gocui.Gui) error {
		v, err := g.View(viewName)
		if err != nil {
			return err
		}
		fmt.Fprintln(v, line)
		return nil
	})
}

func quit(g *gocui.Gui, v *gocui.View) error {
	return gocui.ErrQuit
}

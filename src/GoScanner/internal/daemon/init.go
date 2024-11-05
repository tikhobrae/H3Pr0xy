package daemon

import (
	// "github.com/kardianos/service"
	"github.com/tikhobrae/H3Pr0xy/tree/main/src/GoScanner/common"
)

func init() {
	cfg.Name = common.App
	cfg.DisplayName = common.App
	cfg.Description = "An incredibly fast proxy checker & IP rotator with ease."
	// cfg = &service.Config{
	// 	Name:        common.App,
	// 	DisplayName: common.App,
	// 	Description: "An incredibly fast proxy checker & IP rotator with ease.",
	// }
}

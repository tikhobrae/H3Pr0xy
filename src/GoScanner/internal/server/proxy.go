package server

import (
	"github.com/elazarl/goproxy"
	"github.com/tikhobrae/H3Pr0xy/tree/main/src/GoScanner/common"
)

// Proxy as ServeMux in proxy server handler.
type Proxy struct {
	HTTPProxy *goproxy.ProxyHttpServer
	Options   *common.Options
}

package main

import (
	"errors"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

func fileToString(filePath string) (string, error) {
	content, err := ioutil.ReadFile(filePath)
	if err != nil {
		return "", err
	}
	contentString := string(content)
	return contentString, nil
}

func main() {
	TCPMap := map[string]string{
		"00": "ERROR_STATUS",
		"01": "ESTABLISHED",
		"02": "SYN_SENT",
		"03": "SYN_RECV",
		"04": "FIN_WAIT1",
		"05": "FIN_WAIT2",
		"06": "TIME_WAIT",
		"07": "CLOSE",
		"08": "CLOSE_WAIT",
		"09": "LAST_ACK",
		"0A": "LISTEN",
		"0B": "CLOSING",
	}
	statusMap := make(map[string]int, 0)
	contentString, err := fileToString("./tcp")
	if err != nil {
		log.Fatal(err)
	}
	contentSlice := strings.Split(contentString, "\n")
	for _, line := range contentSlice {
		st := strings.Fields(strings.TrimSpace(line))
		if len(st) < 3 {
			continue
		}
		tcpType := st[3]
		if tcpType == "st" {
			continue
		}
		v, ok := TCPMap[tcpType]
		if ok {
			statusMap[v]++
		}
	}
	if len(os.Args) == 2 {
		var b bool
		for _, v := range TCPMap {
			if os.Args[1] == v {
				b = true
				v, ok := statusMap[os.Args[1]]
				if ok {
					fmt.Printf("%d\n", v)
				} else {
					fmt.Printf("%d\n", 0)
				}
				break
			}
		}
		if !b {
			err := errors.New("unknown tcp parameter")
			log.Fatal(err)
		}
	} else {
		for k, v := range statusMap {
			fmt.Printf("%s: %d\n", k, v)
		}
	}
}


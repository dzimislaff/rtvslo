## RTVSLO

Preprost program, ki dostopa do posnetkov na spletnem portalu rtvslo.si.

### Možnosti
```
{IME_PROGRAMA} [--pomoč/-h] [--verzija] predvajaj/shrani [--id]
```
```
  shrani        shrani posnetek v mapo, v kateri je bil program zagnan  
  predvajaj     predvaja posnetek v predvajalniku  
  --id          ID številka posnetka  
  --pomoč       izpiše pomoč
```
### Primer rabe 
#### Predvajaj posnetek  
```shell
$ rtvslo predvajaj https://4d.rtvslo.si/arhiv/zrcalo-dneva/174612420
```
```shell
$ rtvslo predvajaj --id 174612420
```
#### Shrani posnetek  
```shell
$ rtvslo shrani
```

&nbsp;

SampleInput:

Service in input.yaml
\
label_y1\
format_y1

Each target will have :\
ref_no: 2
\
\
&nbsp;

alertconfig:
``` 
alert_config:
    priority: P2
    message: '(U) Database Connection Utilization (%) is HIGH'
    rule:
      for_duration: 5m
      evaluate_every: 10s
    condition_query:
    - OR,avg,1,now,5m,gt,20
    - OR,avg,2,now,5m,gt,30
```


```
formatY1: (options : Bps ,       bytes , s ,      percent  )
labelY1:  (options : bytes/sec , bytes , seconds, percent )
```




## To run kafka server, use command - 
<br />
$ su -l kafka

## To exit kafka server, use command - 
<br />
$ exit

## To start kafka service, use command - 
<br />
$ sudo systemctl start kafka

## To get status of kafka service, use command - 
<br />
$ sudo systemctl status kafka

## After making changes, to reload kafka and zookeeper, use commands - 
<br />
$ sudo systemctl enable zookeeper
$ sudo systemctl enable kafka

## To get commands for installation and creating new topics, visit - 
<br />
https://hevodata.com/blog/how-to-install-kafka-on-ubuntu/

## Kafka topic commands - 
<br />
Create - $ ~/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic MajorProject --create --partitions 3 --replication-factor 1 <br />
List - $ ~/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list <br />
Delete - $ ~/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic MajorProject

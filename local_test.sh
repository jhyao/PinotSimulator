WORKDIR=/Users/yao/workspace/pinot
# Start zookeeper
$WORKDIR/zookeeper-latest/bin/zkServer.sh start

# Stop zookeeper
$WORKDIR/zookeeper-latest/bin/zkServer.sh stop

# Start kafka
$WORKDIR/kafka-latest/bin/kafka-server-start.sh  $WORKDIR/kafka-latest/config/server.properties > $WORKDIR/logs/kafka.log 2>$WORKDIR/logs/kafka.log &

# Stop kafka
$WORKDIR/kafka-latest/bin/kafka-server-stop.sh

# list topic
$WORKDIR/kafka-latest/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

# create topic
$WORKDIR/kafka-latest/bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic issuerrisk
$WORKDIR/kafka-latest/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic issuerrisk --partitions 1 --replication-factor 1

# Install pinot
TARGET="apache-pinot-20231107-4"
mkdir $TARGET
tar -xvf apache-pinot-1.0.0-bin.tar.gz -C $TARGET --strip-components=1
ln -sfn $TARGET pinot-latest


# Start Pinot
export LOG_ROOT=$WORKDIR/logs
export PINOT_COMPONENT=controller
export JAVA_OPTS="-Xms256M -Xmx256M"
$WORKDIR/pinot-latest/bin/pinot-admin.sh StartController > $WORKDIR/logs/pinot-controller-console.log 2>$WORKDIR/logs/pinot-controller-console.log &

export LOG_ROOT=$WORKDIR/logs
export PINOT_COMPONENT=broker
export JAVA_OPTS="-Xms256M -Xmx256M"
$WORKDIR/pinot-latest/bin/pinot-admin.sh StartBroker > $WORKDIR/logs/pinot-broker-console.log 2>$WORKDIR/logs/pinot-broker-console.log &

export LOG_ROOT=$WORKDIR/logs
export PINOT_COMPONENT=server
export JAVA_OPTS="-Xms256M -Xmx1G"
$WORKDIR/pinot-latest/bin/pinot-admin.sh StartServer > $WORKDIR/logs/pinot-server-console.log 2>$WORKDIR/logs/pinot-server-console.log &


# Delete table
curl -X DELETE http://localhost:9000/tables/issuerrisk_REALTIME
curl -X DELETE http://localhost:9000/schemas/issuerrisk

# Create schema and table
$WORKDIR/pinot-latest/bin/pinot-admin.sh AddTable -tableConfigFile $WORKDIR/Simulator/table_upsert.json -schemaFile $WORKDIR/Simulator/schema.json -exec


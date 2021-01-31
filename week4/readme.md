# **Tuần 4**

## *Tìm hiểu về Spark Properties*

Spark Properties kiểm soát hầu hết các cài đặt và được cấu hình riêng cho từng ứng dụng. Các properties được cài đặt trực tiếp qua SparkConf được đưa vào SparkContext. SparkConf cho phép bạn định cấu hình một số thuộc tính chung (ví dụ: URL chính và tên ứng dụng), giống như các cặp giá trị được đặt qua phương thức `set()`. Ví dụ: chúng ta có thể khởi tạo một ứng dụng với hai luồng như sau:

```
val conf = new SparkConf()
             .setMaster("local[2]")
             .setAppName("CountingSheep")
val sc = new SparkContext(conf)
```

Các thuộc tính liên qua đến thời gian cần được cấu hình với các đơn vị thời gian nhất định

```
25ms (milliseconds)
5s (seconds)
10m or 10min (minutes)
3h (hours)
5d (days)
1y (years)
```

Tương tự với thời gian, kính thước bao gồm các đơn vị sau

```
1b (bytes)
1k or 1kb (kibibytes = 1024 bytes)
1m or 1mb (mebibytes = 1024 kibibytes)
1g or 1gb (gibibytes = 1024 mebibytes)
1t or 1tb (tebibytes = 1024 gibibytes)
1p or 1pb (pebibytes = 1024 tebibytes)
```

### *Dynamically Loading Spark Properties*

Có thể cấu hình ứng dụng sau khi đã khởi động hay vì lý do nào đó mà chúng ta không muốn cố định các giá trị cấu hình từ trước. Chúng ta có thể tải các thuộc tính cấu hình trong thời gian thực thi

Trước khi chạy cần tạo một config rỗng

```
val sc = new SparkContext(new SparkConf())
```

Sau đó, chúng ta có thể cung cấp các giá trị thuộc tính trong thời gian chạy như sau

```
./bin/spark-submit --name "My app" --master local[4] --conf spark.eventLog.enabled=false
  --conf "spark.executor.extraJavaOptions=-XX:+PrintGCDetails -XX:+PrintGCTimeStamps" myApp.jar
```

### *Viewing Spark Properties*

Giao diện người dùng web ứng dụng tại http://<driver>:4040liệt kê các thuộc tính Spark trong tab "Môi trường". Đây là một nơi hữu ích để kiểm tra để đảm bảo rằng các thuộc tính của bạn đã được đặt chính xác. Lưu ý rằng chỉ có giá trị xác định một cách rõ ràng thông qua spark-defaults.conf, SparkConfhoặc dòng lệnh sẽ xuất hiện. Đối với tất cả các thuộc tính cấu hình khác, bạn có thể giả sử giá trị mặc định được sử dụng.

#### **Thuộc tính có sẵn**

Dưới đây là các loại thuộc tính có sẵn trong spark

- Thuộc tính ứng dụng.

- Môi trường thực thi

- Hành vi xáo trộn

- Spark UI

- Nén và tuần tự hóa

- Quản lý bộ nhớ

- Hành vi Thực thi

- Kết nối mạng

- Lập lịch trình

- Phân bổ động

- Bảo vệ

- Cấu hình TLS / SSL

- Spark SQL

- Spark Streaming

- SparkR

- GraphX

- Triển khai

- Người quản lý cụm

[Tìm hiểu thêm](https://spark.apache.org/docs/2.3.0/configuration.html#available-properties)

#### **Các biến môi trường**

Một số cài đặt Spark nhất định có thể được định cấu hình thông qua các biến môi trường, được đọc từ conf/spark-env.shtập lệnh trong thư mục nơi Spark được cài đặt (hoặc conf/spark-env.cmdtrên Windows). Ở chế độ Độc lập và Mesos, tệp này có thể cung cấp thông tin cụ thể cho máy như tên máy chủ. Nó cũng có nguồn gốc khi chạy các ứng dụng Spark cục bộ hoặc các tập lệnh gửi.

Lưu ý rằng conf/spark-env.shkhông tồn tại theo mặc định khi Spark được cài đặt. Tuy nhiên, bạn có thể sao chép conf/spark-env.sh.templateđể tạo nó. Đảm bảo rằng bạn thực thi bản sao.

Các biến sau có thể được đặt trong spark-env.sh:

- **JAVA_HOME :** Vị trí nơi Java được cài đặt (nếu nó không ở trên mặc định của bạn PATH).

- **PYSPARK_PYTHON :** Thực thi nhị phân Python để sử dụng cho PySpark trong cả trình điều khiển và công nhân (mặc định là python2.7nếu có, nếu không python). Thuộc tính spark.pyspark.pythonđược ưu tiên nếu nó được đặt

- **PYSPARK_DRIVER_PYTHON :** Thực thi nhị phân Python để chỉ sử dụng cho PySpark trong trình điều khiển (mặc định là PYSPARK_PYTHON). Thuộc tính spark.pyspark.driver.pythonđược ưu tiên nếu nó được đặt

- **SPARKR_DRIVER_R :** R binary thực thi để sử dụng cho SparkR shell (mặc định là R). Thuộc tính spark.r.shell.commandđược ưu tiên nếu nó được đặt

- **SPARK_LOCAL_IP :** Địa chỉ IP của máy để liên kết.

- **SPARK_PUBLIC_DNS :** Tên máy chủ chương trình Spark của bạn sẽ quảng cáo đến các máy khác.



## *Tìm hiểu về RDD*

### *RDD (Tập dữ liệu phân tán đàn hồi) là gì?*

**_RDD_** (Tập dữ liệu phân tán có khả năng phục hồi) là một khối xây dựng cơ bản của PySpark, là tập hợp các đối tượng phân tán không thay đổi, chịu được lỗi. Bất biến nghĩa là bạn không thể thay đổi nó. Mỗi bản ghi trong RDD được chia thành các phân vùng logic, có thể được tính toán trên các nút khác nhau của cụm. 

Nói cách khác, RDD là một tập hợp các đối tượng tương tự như danh sách trong Python, với sự khác biệt là RDD được tính toán trên một số quy trình nằm rải rác trên nhiều máy chủ vật lý còn được gọi là các nút trong một cụm trong khi tập hợp Python tồn tại và xử lý chỉ trong một quy trình.

Ngoài ra, RDD cung cấp sự trừu tượng hóa dữ liệu của việc phân vùng và phân phối dữ liệu được thiết kế để chạy tính toán song song trên một số nút, trong khi thực hiện các phép biến đổi trên RDD, chúng ta không phải lo lắng về tính song song như PySpark cung cấp theo mặc định.

Lưu ý: RDD có thể có tên và số nhận dạng duy nhất (id)

### *Lợi ích của PySpark RDD*

PySpark được thích nghi rộng rãi trong cộng đồng Học máy và Khoa học dữ liệu do những ưu điểm của nó so với lập trình python truyền thống.

#### **Xử lý trong bộ nhớ**

**_PySpark_** tải dữ liệu từ đĩa và xử lý trong bộ nhớ và giữ dữ liệu trong bộ nhớ, đây là điểm khác biệt chính giữa PySpark và Mapreduce (I / O chuyên sâu). Giữa các lần biến đổi, chúng ta cũng có thể lưu cache / duy trì RDD trong bộ nhớ để sử dụng lại các tính toán trước đó.

#### **Bất biến**

PySpark RDD có nghĩa là bất biến về bản chất, một khi RDD được tạo, bạn không thể sửa đổi. Khi chúng ta áp dụng các phép biến đổi trên RDD, PySpark sẽ tạo ra một RDD mới và duy trì Dòng dõi RDD.

#### **Khả năng chịu lỗi**

PySpark hoạt động trên các kho dữ liệu có khả năng chịu lỗi trên HDFS, S3, v.v. do đó bất kỳ hoạt động RDD nào không thành công, nó sẽ tự động tải lại dữ liệu từ các phân vùng khác. Ngoài ra, Khi các ứng dụng PySpark chạy trên một cụm, các lỗi tác vụ PySpark sẽ tự động được khôi phục trong một số lần nhất định (theo cấu hình) và kết thúc ứng dụng một cách liền mạch.

#### **Tiến hóa lười biếng**

PySpark không đánh giá các phép biến đổi RDD khi chúng xuất hiện / gặp phải bởi Driver thay vào đó nó giữ tất cả các phép biến đổi khi nó gặp (DAG) và đánh giá tất cả các phép biến đổi khi nó thấy hành động RDD đầu tiên.

#### **Phân vùng**

Khi bạn tạo RDD từ một dữ liệu, nó theo mặc định phân vùng các phần tử trong RDD. Theo mặc định, nó phân vùng theo số lượng lõi có sẵn.

### *Hạn chế của PySpark RDD*

PySpark RDD không phù hợp nhiều với các ứng dụng thực hiện cập nhật cho kho lưu trữ trạng thái, chẳng hạn như hệ thống lưu trữ cho ứng dụng web. Đối với các ứng dụng này, sẽ hiệu quả hơn nếu sử dụng các hệ thống thực hiện ghi nhật ký cập nhật truyền thống và kiểm tra dữ liệu, chẳng hạn như cơ sở dữ liệu. Mục tiêu của RDD là cung cấp một mô hình lập trình hiệu quả cho phân tích hàng loạt và loại bỏ các ứng dụng không đồng bộ này.

### *Tạo RDD*

RDD được tạo ra chủ yếu theo hai cách khác nhau,

- Song song hóa một bộ sưu tập hiện có và tham khảo một tập dữ liệu trong một hệ thống bên ngoài lưu trữ ( `HDFS`, `S3` và nhiều hơn nữa).

- Trước khi chúng ta xem xét các ví dụ, trước tiên hãy khởi tạo SparkSession bằng phương thức mẫu xây dựng được định nghĩa trong lớp SparkSession. Trong khi khởi tạo, chúng ta cần cung cấp tên chính và ứng dụng như hình bên dưới. Trong ứng dụng thời gian thực, bạn sẽ vượt qua master từ spark-submit thay vì hardcoding trên ứng dụng Spark.

```
from pyspark.sql import SparkSession
spark:SparkSession = SparkSession.builder()
      .master("local[1]")
      .appName("SparkByExamples.com")
      .getOrCreate()    
```

- *master()* - Nếu bạn đang chạy nó trên cụm, bạn cần sử dụng tên chính của mình làm đối số cho chủ (). thông thường, nó sẽ là một trong hai  yarn (Yet Another Resource Negotiator)hoặc  mesos tùy thuộc vào thiết lập cụm của bạn.

- - Sử dụng local[x]khi chạy ở chế độ Độc lập. x phải là một giá trị nguyên và phải lớn hơn 0; điều này thể hiện số lượng phân vùng nó sẽ tạo khi sử dụng RDD, DataFrame và Dataset. Lý tưởng nhất, giá trị x phải là số lõi CPU bạn có.

- *appName()* - Được sử dụng để đặt tên ứng dụng của bạn.

- *getOrCreate()* - Điều này trả về một đối tượng SparkSession nếu đã tồn tại, tạo một đối tượng mới nếu chưa tồn tại.

Lưu ý: Tạo đối tượng SparkSession , nội bộ nó tạo một SparkContext cho mỗi JVM.

#### **Tạo RDD bằng sparkContext.parallelize()**

Bằng cách sử dụng `parallelize()` hàm của `SparkContext ( sparkContext.parallelize () )`, bạn có thể tạo RDD. Hàm này tải bộ sưu tập hiện có từ chương trình trình điều khiển của bạn vào song song hóa RDD. Đây là phương pháp cơ bản để tạo RDD và được sử dụng khi bạn đã có dữ liệu trong bộ nhớ được tải từ tệp hoặc từ cơ sở dữ liệu. và nó yêu cầu tất cả dữ liệu phải có trên chương trình trình điều khiển trước khi tạo RDD.

![Hướng dẫn Pyspark rdd](https://ngominhtoan.github.io/colab_massive_data/week4/pic1.webp)

#### **RDD từ danh sách**

```
# Create RDD from parallelize  
data = [1,2,3,4,5,6,7,8,9,10,11,12]
rdd=spark.sparkContext.parallelize(data)
```

Đối với các ứng dụng sản xuất, chúng tôi chủ yếu là tạo RDD bằng cách sử dụng hệ thống lưu trữ bên ngoài như `HDFS`, `S3`, `HBasevv` Để làm cho nó đơn giản cho PySpark RDD này hướng dẫn chúng ta đang sử dụng tập tin từ hệ thống địa phương hoặc tải nó từ danh sách python để tạo RDD.

#### **Tạo RDD bằng sparkContext.textFile ()**

Sử dụng [phương thức textFile (), chúng ta có thể đọc tệp văn bản](https://sparkbyexamples.com/spark/spark-read-text-file-rdd-dataframe/) (.txt) vào RDD.

```
#Create RDD from external Data source
rdd2 = spark.sparkContext.textFile("/path/textFile.txt")
```

#### **Tạo RDD bằng sparkContext.wholeTextFiles ()**

[Hàm wholeTextFiles ()](https://sparkbyexamples.com/spark/spark-read-text-file-rdd-dataframe/) trả về một [PairRDD](https://sparkbyexamples.com/apache-spark-rdd/spark-pair-rdd-functions/) với khóa là đường dẫn tệp và giá trị là nội dung tệp.

```
#Reads entire file into a RDD as single record.
rdd3 = spark.sparkContext.wholeTextFiles("/path/textFile.txt")
```

Bên cạnh việc sử dụng các tệp văn bản, chúng ta cũng có thể [tạo RDD từ tệp CSV](https://sparkbyexamples.com/pyspark/pyspark-read-csv-file-into-dataframe/) , JSON và nhiều định dạng khác.

#### **Tạo RDD trống bằng sparkContext.emptyRDD**

Sử dụng `emptyRDD()` phương thức trên sparkContext, chúng ta có thể [tạo một RDD không có dữ liệu](https://sparkbyexamples.com/spark/spark-how-to-create-an-empty-rdd/) . Phương pháp này tạo ra một RDD trống không có phân vùng.

```
# Creates empty RDD with no partition    
rdd = spark.sparkContext.emptyRDD 
# rddString = spark.sparkContext.emptyRDD[String]
```

#### **Tạo RDD trống với phân vùng**

Đôi khi, chúng ta có thể cần ghi RDD trống vào các tệp theo phân vùng, Trong trường hợp này, bạn nên tạo RDD trống có phân vùng.

```
#Create empty RDD with partition
rdd2 = spark.sparkContext.parallelize([],10) #This creates 10 partitions
```

### *RDD Song song hóa*

Khi chúng ta sử dụng `parallelize()` hoặc `textFile()` hoặc  `wholeTextFiles()` các phương thức của [SparkContxt](https://sparkbyexamples.com/pyspark/pyspark-what-is-sparksession/) để khởi tạo RDD, nó sẽ tự động chia dữ liệu thành các phân vùng dựa trên tính khả dụng của tài nguyên. khi bạn chạy nó trên máy tính xách tay, nó sẽ tạo các phân vùng có cùng số lượng lõi có sẵn trên hệ thống của bạn.

**getNumPartitions ()** - Đây là một hàm RDD trả về một số phân vùng mà tập dữ liệu của chúng tôi được chia thành.

```
print("initial partition count:"+str(rdd.getNumPartitions()))
#Outputs: initial partition count:2
```

**Đặt song song theo cách thủ công** - Chúng ta cũng có thể đặt một số phân vùng theo cách thủ công, tất cả những gì chúng ta cần là chuyển một số phân vùng làm tham số thứ hai cho các hàm này chẳng hạn   `sparkContext.parallelize([1,2,3,4,56,7,8,9,12,3], 10)`. 

### *Phân vùng lại và kết hợp*

Đôi khi chúng ta có thể cần phải [phân vùng lại RDD](https://sparkbyexamples.com/pyspark/pyspark-repartition-vs-coalesce/) , PySpark cung cấp hai cách để phân vùng lại; đầu tiên sử dụng `repartition()` phương pháp xáo trộn dữ liệu từ tất cả các nút còn được gọi là xáo trộn đầy đủ và phương thức [Coalesce ()](https://sparkbyexamples.com/pyspark/pyspark-repartition-vs-coalesce/) thứ hai [trộn](https://sparkbyexamples.com/spark/spark-shuffle-partitions/) dữ liệu từ các nút tối thiểu, ví dụ: nếu bạn có dữ liệu trong 4 phân vùng và thực hiện việc `coalesce(2)` di chuyển dữ liệu chỉ từ 2 nút.  

Cả hai hàm đều lấy số lượng phân vùng để phân vùng lại rdd như hình dưới đây. Lưu ý rằng [repartition()](https://sparkbyexamples.com/pyspark/pyspark-repartition-vs-coalesce/) phương pháp là một hoạt động rất tốn kém vì nó xáo trộn dữ liệu từ tất cả các nút trong một cụm. 

```
reparRdd = rdd.repartition(4)
print("re-partition count:"+str(reparRdd.getNumPartitions()))
#Outputs: "re-partition count:4
```

**Lưu ý:** các phương thức repartition () hoặc thanesce () cũng trả về một RDD mới.

### *Hoạt động PySpark RDD*

**Các phép biến đổi RDD** - Các phép biến  đổi là các hoạt động lười biếng, thay vì cập nhật một RDD, các phép toán này trả về một RDD khác.

**Các hành động RDD** - các  hoạt động kích hoạt tính toán và trả về giá trị RDD.

#### **Biến đổi RDD với ví dụ**

[Các phép biến đổi trên PySpark RDD](https://sparkbyexamples.com/pyspark/pyspark-rdd-transformations/) trả về một RDD khác và các phép biến đổi là lười biếng nghĩa là chúng không thực thi cho đến khi bạn gọi một hành động trên RDD. Một số biến đổi trên RDD của là `flatMap()`, `map()`, `reduceByKey()`, `filter()`, `sortByKey()` và trở RDD mới thay vì cập nhật hiện hành.

Trong phần Chuyển đổi PySpark RDD của hướng dẫn này, tôi sẽ giải thích các phép biến đổi bằng cách sử dụng ví dụ đếm từ. Hình ảnh dưới đây minh họa các phép biến đổi RDD khác nhau mà chúng ta sẽ sử dụng.

Đầu tiên, tạo một RDD bằng cách đọc một tệp văn bản. Tệp văn bản được sử dụng ở đây có sẵn tại   dự án [GitHub](https://github.com/spark-examples/spark-scala-examples/blob/master/src/main/resources/test.txt) .

```
rdd = spark.sparkContext.textFile("/tmp/test.txt")
```

**flatMap** -  `flatMap()` phép biến đổi làm phẳng RDD sau khi áp dụng hàm và trả về một RDD mới. Trong ví dụ dưới đây, đầu tiên, nó chia từng bản ghi theo không gian trong RDD và cuối cùng làm phẳng nó. Kết quả RDD bao gồm một từ duy nhất trên mỗi bản ghi.

```
rdd2 = rdd.flatMap(lambda x: x.split(" "))
```

**map** - `map()` biến đổi được sử dụng để áp dụng bất kỳ hoạt động phức tạp nào như thêm cột, cập nhật cột, v.v., đầu ra của phép biến đổi bản đồ sẽ luôn có cùng số bản ghi như đầu vào.

Trong ví dụ đếm từ của chúng tôi, chúng tôi đang thêm một cột mới với giá trị 1 cho mỗi từ, kết quả của RDD là `PairRDDFunctions` chứa các cặp khóa-giá trị, từ thuộc loại Chuỗi là Khóa và 1 thuộc loại Int là giá trị.

```
rdd3 = rdd2.map(lambda x: (x,1))
```

**ReduceByKey** -  `reduceByKey()` hợp nhất các giá trị cho mỗi khóa với chức năng được chỉ định. Trong ví dụ của chúng tôi, nó làm giảm chuỗi từ bằng cách áp dụng hàm sum trên giá trị. Kết quả RDD của chúng tôi chứa các từ duy nhất và số lượng của chúng. 

```
rdd5 = rdd4.reduceByKey(lambda a,b: a+b)
```

**sortByKey** -  `sortByKey()` phép biến đổi được sử dụng để sắp xếp các phần tử RDD trên khóa. Trong ví dụ của chúng tôi, đầu tiên, chúng tôi chuyển đổi RDD [(String, Int]) thành RDD [(Int, String]) bằng cách sử dụng phép biến đổi bản đồ và áp dụng sortByKey mà lý tưởng là sắp xếp trên một giá trị số nguyên. Và cuối cùng, câu lệnh foreach với println trả về tất cả các từ trong RDD và số lượng của chúng là cặp khóa-giá trị

```
rdd6 = rdd5.map(lambda x: (x[1],x[0])).sortByKey()
#Print rdd6 result to console
print(rdd6.collect())
```

**filter()** được sử dụng để lọc các bản ghi trong RDD. Trong ví dụ của chúng tôi, chúng tôi đang lọc tất cả các từ bắt đầu bằng “a”.

```
rdd4 = rdd3.filter(lambda x : 'an' in x[1])
print(rdd4.collect())
```

## *Tìm hiểu về DataFrame*

### *DataFrame là gì?*

DataFrame là một kiểu dữ liệu collection phân tán, được tổ chức thành các cột được đặt tên. Về mặt khái niệm, nó tương đương với các bảng quan hệ (relational tables) đi kèm với các kỹ thuật tối ưu tính toán.

![Create DataFrame](https://ngominhtoan.github.io/colab_massive_data/week4/pic2.jpg)

### *Tạo DataFrame*

#### **Tạo DataFrame từ RDD**

Một cách dễ dàng để tạo PySpark DataFrame là từ một RDD hiện có. đầu tiên, hãy tạo một Spark RDD từ một Danh sách bộ sưu tập bằng cách gọi hàm song song () từ SparkContext . Chúng tôi sẽ cần đối tượng rdd này cho tất cả các ví dụ của chúng tôi bên dưới.

```
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
rdd = spark.sparkContext.parallelize(data)
```

##### **Sử dụng hàm toDF()**

Phương thức toDF () của PySpark RDD được sử dụng để tạo DataFrame từ RDD hiện có. Vì RDD không có cột, DataFrame được tạo với tên cột mặc định “_1” và “_2” vì chúng ta có hai cột.

```
dfFromRDD1 = rdd.toDF()
dfFromRDD1.printSchema()
```

printchema () cho ra kết quả bên dưới.

```
root
 |-- _1: string (nullable = true)
 |-- _2: string (nullable = true)
```

Nếu bạn muốn cung cấp tên cột cho toDF() phương pháp sử dụng DataFrame với tên cột làm đối số như hình dưới đây.

```
columns = ["language","users_count"]
dfFromRDD1 = rdd.toDF(columns)
dfFromRDD1.printSchema()
```

Điều này tạo ra lược đồ của DataFrame với các tên cột.

```
root
 |-- language: string (nullable = true)
 |-- users: string (nullable = true)
```

Theo mặc định, kiểu dữ liệu của các cột này suy ra kiểu dữ liệu. Chúng ta có thể thay đổi hành vi này bằng cách cung cấp lược đồ , trong đó chúng ta có thể chỉ định tên cột, kiểu dữ liệu và giá trị có thể làm trống cho mỗi trường / cột.

##### **Sử dụng createDataFrame () từ SparkSession**

Sử dụng createDataFrame () từ SparkSession là một cách khác để tạo và nó lấy đối tượng rdd làm đối số. và chuỗi với toDF () để chỉ định tên cho các cột.

```
dfFromRDD2 = spark.createDataFrame(rdd).toDF(*columns)
```

#### **Tạo DataFrame từ list dữ liệu**

Trong phần này, chúng ta sẽ xem cách tạo PySpark DataFrame từ một danh sách. Những ví dụ này sẽ tương tự như những gì chúng ta đã thấy trong phần trên với RDD, nhưng chúng ta sử dụng đối tượng dữ liệu danh sách thay vì đối tượng “rdd” để tạo DataFrame.

##### **Sử dụng createDataFrame () từ SparkSession**

Gọi `createDataFrame()` from `SparkSession` là một cách khác để tạo PySpark DataFrame, nó lấy một đối tượng danh sách làm đối số. và chuỗi với `0toDF()` để chỉ định tên cho các cột.

```
dfFromData2 = spark.createDataFrame(data).toDF(*columns)
```

##### **Sử dụng createDataFrame () với kiểu Hàng**

`createDataFrame()` có một chữ ký khác trong PySpark lấy bộ sưu tập kiểu Hàng và lược đồ cho tên cột làm đối số. Để sử dụng điều này, trước tiên chúng ta cần chuyển đổi đối tượng “dữ liệu” từ danh sách sang danh sách Hàng.

```
rowData = map(lambda x: Row(*x), data) 
dfFromData3 = spark.createDataFrame(rowData,columns)
```

##### **Tạo DataFrame bằng lược đồ**

Nếu bạn muốn chỉ định tên cột cùng với kiểu dữ liệu của chúng, trước tiên bạn nên tạo lược đồ StructType và sau đó gán nó trong khi tạo DataFrame.

```
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
data2 = [("James","","Smith","36636","M",3000),
    ("Michael","Rose","","40288","M",4000),
    ("Robert","","Williams","42114","M",4000),
    ("Maria","Anne","Jones","39192","F",4000),
    ("Jen","Mary","Brown","","F",-1)
  ]

schema = StructType([ \
    StructField("firstname",StringType(),True), \
    StructField("middlename",StringType(),True), \
    StructField("lastname",StringType(),True), \
    StructField("id", StringType(), True), \
    StructField("gender", StringType(), True), \
    StructField("salary", IntegerType(), True) \
  ])
 
df = spark.createDataFrame(data=data2,schema=schema)
df.printSchema()
df.show(truncate=False)
```

Điều này dẫn đến sản lượng thấp hơn.

```
root
 |-- firstname: string (nullable = true)
 |-- middlename: string (nullable = true)
 |-- lastname: string (nullable = true)
 |-- id: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- salary: integer (nullable = true)

+---------+----------+--------+-----+------+------+
|firstname|middlename|lastname|id   |gender|salary|
+---------+----------+--------+-----+------+------+
|James    |          |Smith   |36636|M     |3000  |
|Michael  |Rose      |        |40288|M     |4000  |
|Robert   |          |Williams|42114|M     |4000  |
|Maria    |Anne      |Jones   |39192|F     |4000  |
|Jen      |Mary      |Brown   |     |F     |-1    |
+---------+----------+--------+-----+------+------+
```

#### **Tạo DataFrame từ tệp dữ liệu**

Trong thời gian thực, hầu hết bạn tạo DataFrame từ các tệp nguồn dữ liệu như CSV, Văn bản, JSON, XML, v.v.

PySpark theo mặc định hỗ trợ nhiều định dạng dữ liệu mà không cần nhập bất kỳ thư viện nào và để tạo DataFrame, bạn cần sử dụng phương pháp thích hợp có sẵn trong `DataFrameReader` lớp.

##### **Tạo DataFrame từ CSV**

Sử dụng `csv()` phương thức của `DataFrameReader` đối tượng để tạo DataFrame từ tệp CSV. bạn cũng có thể cung cấp các tùy chọn như dấu phân cách sẽ sử dụng, cho dù bạn đã trích dẫn dữ liệu, định dạng ngày tháng, lược đồ suy luận, v.v. Vui lòng tham khảo PySpark Read CSV thành DataFrame

```
df2 = spark.read.csv("/src/resources/file.csv")
```

##### **Tạo từ tệp văn bản (TXT)**

Tương tự, bạn cũng có thể tạo DataFrame bằng cách đọc từ tệp Văn bản, sử dụng `text()` phương thức của DataFrameReader để làm như vậy.

```
df2 = spark.read.text("/src/resources/file.txt")
```

##### **Tạo từ tệp JSON**

PySpark cũng được sử dụng để xử lý các tệp dữ liệu bán cấu trúc như định dạng JSON. bạn có thể sử dụng json()phương thức của DataFrameReader để đọc tệp `JSON` vào DataFrame. Dưới đây là một ví dụ đơn giản.

```
df2 = spark.read.json("/src/resources/file.json")
```

Tương tự, chúng ta có thể tạo DataFrame trong PySpark từ hầu hết các cơ sở dữ liệu quan hệ mà tôi chưa trình bày ở đây và tôi sẽ để bạn khám phá.



## Tài liệu tham khảo

1. [Spark RDD](https://sparkbyexamples.com/pyspark-rdd)

2. [Spark Properties](https://spark.apache.org/docs/latest/configuration.html)

3. [Spark DataFrame](https://sparkbyexamples.com/pyspark/different-ways-to-create-dataframe-in-pyspark/)

_ Edit by **Ngô Minh Toàn**_

# Audit Logs
 
## Introduction
 
Hopsworks collects audit logs on all URL requests to the application server. These logs are saved in Payara log directory
under ```<payara-log-dir>/audit``` by default.
 
## Prerequisites
To follow this guide you need to have:
 
- an administrator account on the Hopsworks cluster.
- ssh access to the Hopsworks cluster.
 
## Step 1: Configure Audit log
 
Audit logs can be configured from the _Cluster Settings_ Configuration tab.
You can access the _Configuration_ page of your Hopsworks cluster by clicking on your name, in the top right corner, and choosing _Cluster Settings_ from the dropdown menu.
 
<figure>
 <a  href="../../../assets/images/admin/audit/audit-log-vars.png">
   <img src="../../../assets/images/admin/audit/audit-log-vars.png" alt="Audit log configuration" />
 </a>
 <figcaption>Audit log configuration</figcaption>
</figure>
 
Type _audit_ in the find variable search box to see the configuration variables associated with audit logs.
You can click on the edit button (:pencil2:) of the variable you want to edit and change the value. Click
on the check mark to save the new value.
 
Available configurable variables for audit logs are:
 
1. audit_log_count: the number of files to keep when rotating logs (java.util.logging.FileHandler.count)
2. audit_log_dir: the path where audit logs are saved.
3. audit_log_file_format: log file name pattern. (java.util.logging.FileHandler.pattern)
4. audit_log_file_type: the output format of the log file.
Can be one of java.util.logging.SimpleFormatter (default), io.hops.hopsworks.audit.helper.JSONLogFormatter, or io.hops.hopsworks.audit.helper.HtmlLogFormatter.
5. audit_log_size_limit: the maximum number of bytes to write to any one file. (java.util.logging.FileHandler.limit)
6. audit_log_date_format: if io.hops.hopsworks.audit.helper.JSONLogFormatter is used as audit log file type, this will set the date format of the output JSON.
The format should be java.text.SimpleDateFormat compatible string.
 
Changes made to audit log configurations need a reload of _hopsworks-ear_.
To reload hopsworks go to the payara admin ```https://domain:4848```, after you log in click on _Aplications_ on the side menu.
From the list of deployed applications select _hopsworks-ear_ and click on the reload action.
 
 
## Step 2: Access the Logs
 
To access the audit logs ssh into the head node of your Hopsworks cluster and navigate to the path set in _audit\_log\_dir_.
 
A line of output from an audit log with JSONLogFormatter is shown bellow.
 
```json
{"className":"io.hops.hopsworks.api.user.AuthService","methodName":"login","parameters":"[admin@hopsworks.ai, org.apache.catalina.connector.ResponseFacade@2de6dd0b, org.apache.catalina.connector.RequestFacade@7a82f674]","outcome":"200","caller":{"username":null,"email":"admin@hopsworks.ai","userId":null},"clientIp":"10.0.2.2","userAgent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36","pathInfo":"/auth/login","dateTime":"2022-11-09 12:00:08"}
```
 
- className: the class called by the request.
- methodName: the method called by the request.
- parameters: parameters sent from the client.
- outcome: response code sent from the server.
- caller: the logged in user that made the request. Can be username, email, or userId.
- clientIp: the IP address of the client.
- userAgent: the browser used by the client.
- pathInfo: the URL path called by the client.
- dateTime: time of the request.
 
## Conclusion
In this guide you learned how to configure Audit log from the Hopsworks admin page and access the audit log files.

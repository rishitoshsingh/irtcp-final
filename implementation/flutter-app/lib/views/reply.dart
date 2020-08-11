import 'dart:convert';
import 'dart:ffi';

import 'package:flutter/material.dart';
import 'package:hello/presentation/custom_icons_icons.dart';
import 'package:intl/intl.dart';
import 'package:twitter_api/twitter_api.dart';
import 'package:http/http.dart' as http;
import 'dart:developer';
// import 'package:logs/logs.dart';

import '../models/tweets.dart';
import '../strings.dart';

// final Log httpLog = Log('http');

final _twitterOauth = new twitterApi(
    consumerKey: "your key",
    consumerSecret: "your key",
    token: "your key",
    tokenSecret: "your key");

class Reply extends StatelessWidget {
  final Documents tweet;
  Reply({this.tweet});

  var message = "";

  Future<Void> _sendReply(
      String tweetId, String username, String message) async {
    Future twitterRequest = _twitterOauth.getTwitterRequest(
      // Http Method
      "POST",
      "statuses/update.json",
      options: {
        "status": '@' + username + ' ' + message,
        "in_reply_to_status_id": tweetId,
      },
    );
    var res = await twitterRequest;
  }

  Future<Void> _sendReplyToDb(String tweetId, String message) async {
    final response = await http.post(
      Strings.sendReplyToDbBaseUrl,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{"tweet_id": tweetId, "reply": message}),
    );
    if (response.statusCode == 200) {
      log("Successful API $response.toString()");
    } else {
      log("Successful API $response.toString()");
      throw Exception('Can\'t Connect');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.blue,
        padding: EdgeInsets.fromLTRB(16.0, 16.0, 16.0, 16.0),
        child: ListView(
          children: <Widget>[
            Stack(
              children: [
                Align(
                  alignment: Alignment.topRight,
                  child: Container(
                    // padding: EdgeInsets.all(24.0),
                    child: Icon(
                      CustomIcons.twitter,
                      color: Colors.white,
                      size: 100.0,
                    ),
                  ),
                ),
                Align(
                  alignment: Alignment.topLeft,
                  child: Container(
                    child: IconButton(
                      icon: Icon(Icons.arrow_back),
                      color: Colors.white,
                      iconSize: 48.0,
                      onPressed: () {
                        Navigator.pop(context);
                      },
                    ),
                  ),
                ),
                Align(
                  alignment: Alignment.topLeft,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      SizedBox(height: 100.0),
                      RichText(
                        text: TextSpan(
                          text: DateFormat('MMMM d, y').format(
                              DateTime.fromMillisecondsSinceEpoch(
                                  int.parse(tweet.timestamp.date.numberLong))),
                          style: TextStyle(
                            fontSize: 30.0,
                            fontWeight: FontWeight.w500,
                            color: Colors.white,
                          ),
                        ),
                      ),
                      SizedBox(
                        height: 14.0,
                      ),
                      Row(
                        children: <Widget>[
                          Container(
                            padding: EdgeInsets.all(8.0),
                            child: CircleAvatar(
                              backgroundColor: Colors.blue,
                              radius: 30.0,
                              child: CircleAvatar(
                                backgroundImage:
                                    NetworkImage(tweet.profileImageUrl),
                                radius: 30.0,
                              ),
                            ),
                          ),
                          RichText(
                            text: TextSpan(
                              text: '@' + tweet.username + ' ',
                              style: TextStyle(
                                fontSize: 34,
                                fontWeight: FontWeight.w500,
                                color: Colors.white,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                )
              ],
            ),
            Card(
              shadowColor: Colors.black,
              shape: RoundedRectangleBorder(
                side: BorderSide(color: Colors.blue),
                borderRadius: BorderRadius.circular(16.0),
              ),
              elevation: 18.0,
              child: Container(
                padding: EdgeInsets.all(8.0),
                child: Text(
                  utf8.decode(tweet.tweet.toString().codeUnits),
                  style: TextStyle(
                      fontSize: 38.0,
                      fontWeight: FontWeight.w900,
                      fontStyle: FontStyle.italic,
                      color: Colors.deepOrangeAccent[200],
                      fontFamily: 'Open Sans'),
                ),
              ),
            ),
            SizedBox(
              height: 14.0,
            ),
            Row(
              children: <Widget>[
                Container(
                  padding: EdgeInsets.all(8.0),
                  child: CircleAvatar(
                    backgroundColor: Colors.blue,
                    radius: 30.0,
                    child: CircleAvatar(
                      backgroundImage: AssetImage('assets/logo.png'),
                      radius: 30.0,
                    ),
                  ),
                ),
                RichText(
                  text: TextSpan(
                    text: '@IndianRailways ',
                    style: TextStyle(
                      fontSize: 34,
                      fontWeight: FontWeight.w500,
                      color: Colors.white,
                    ),
                  ),
                ),
              ],
            ),
            Card(
              shadowColor: Colors.black,
              shape: RoundedRectangleBorder(
                side: BorderSide(color: Colors.blue),
                borderRadius: BorderRadius.circular(16.0),
              ),
              elevation: 18.0,
              child: Container(
                padding: EdgeInsets.all(8.0),
                child: TextField(
                  autocorrect: true,
                  maxLength: 240,
                  maxLines: null,
                  onChanged: (text) {
                    message = text;
                  },
                  onSubmitted: (text) {
                    message = text;
                  },
                  keyboardType: TextInputType.multiline,
                  textInputAction: TextInputAction.send,
                  textCapitalization: TextCapitalization.sentences,
                  textAlign: TextAlign.justify,
                  decoration: InputDecoration.collapsed(hintText: 'Your Reply'),
                  style: TextStyle(
                      fontSize: 38.0,
                      fontWeight: FontWeight.w900,
                      fontStyle: FontStyle.italic,
                      color: Colors.blue,
                      fontFamily: 'Open Sans'),
                ),
              ),
            ),
            SizedBox(
              height: 14.0,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                FloatingActionButton.extended(
                  onPressed: () {
                    _sendReply(tweet.tweetId, 'RishitoshS', message);
                    _sendReplyToDb(tweet.tweetId, message);
                    Future.delayed(const Duration(milliseconds: 500), () {
                      Navigator.pop(context);
                    });
                  },
                  backgroundColor: Colors.deepOrangeAccent[200],
                  label: Text('Send'),
                  icon: Icon(
                    CustomIcons.send,
                    color: Colors.white,
                  ),
                )
              ],
            ),
          ],
        ),
      ),
    );
  }
}

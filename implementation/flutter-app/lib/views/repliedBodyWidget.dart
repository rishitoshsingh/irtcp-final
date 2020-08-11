import 'package:flutter/material.dart';
import 'package:hello/presentation/custom_icons_icons.dart';
import 'package:hello/strings.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/repliedTweets.dart';
import './reply.dart';

class RepliedBodyWidget extends StatefulWidget {
  final String collection;
  RepliedBodyWidget(this.collection);

  @override
  State<StatefulWidget> createState() => RepliedBodyWidgetState(collection);
}

class RepliedBodyWidgetState extends State<RepliedBodyWidget> {
  Future<RepliedTweets> futureTweets;
  String collection;
  RepliedBodyWidgetState(this.collection);

  @override
  void initState() {
    super.initState();
    futureTweets = _fetchTweets(collection);
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: FutureBuilder(
        future: futureTweets,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return ListView.builder(
              itemCount: snapshot.data.documents.length,
              itemBuilder: (context, position) {
                return getTweetView(context, snapshot.data.documents[position],
                    snapshot.data.documents);
              },
            );
          }
          return CircularProgressIndicator();
        },
      ),
    );
  }
}

Future<RepliedTweets> _fetchTweets(String collection) async {
  final response = await http
      .get(Strings.fetchDocumentsBaseUrl + 'collection=' + collection);
  if (response.statusCode == 200) {
    return RepliedTweets.fromJson(json.decode(response.body));
  } else {
    throw Exception('Can\'t Connect');
  }
}

Widget getTweetView(
    BuildContext context, Documents tweetDoc, List<Documents> documents) {
  return Card(
    shadowColor: Colors.black,
    shape: RoundedRectangleBorder(
      side: BorderSide(color: Colors.blue),
      borderRadius: BorderRadius.circular(16.0),
    ),
    margin: EdgeInsets.fromLTRB(16.0, 8.0, 16.0, 8.0),
    color: Colors.white,
    elevation: 8.0,
    child: Column(
      children: <Widget>[
        Row(
          children: <Widget>[
            Container(
              padding: EdgeInsets.all(8.0),
              child: CircleAvatar(
                backgroundColor: Colors.blue,
                radius: 25.0,
                child: CircleAvatar(
                  backgroundImage: NetworkImage(tweetDoc.profileImageUrl),
                  radius: 24.0,
                ),
              ),
            ),
            Expanded(
              child: Text(
                '@' + tweetDoc.username,
                textScaleFactor: 1.5,
                style: TextStyle(
                  color: Colors.blue,
                ),
              ),
            ),
            Container(
              padding: EdgeInsets.all(16.0),
              child: Text(
                DateTime.now()
                        .difference(DateTime.fromMicrosecondsSinceEpoch(
                            int.parse(tweetDoc.timestamp.date.numberLong) *
                                1000))
                        .inDays
                        .toString() +
                    'd',
                style: TextStyle(color: Colors.grey),
              ),
            ),
          ],
        ),
        Container(
          padding: EdgeInsets.fromLTRB(8.0, 0, 8.0, 8.0),
          child: Text(
            utf8.decode(tweetDoc.tweet.toString().codeUnits),
            style: TextStyle(
              fontStyle: FontStyle.italic,
              fontWeight: FontWeight.w900,
              color: Colors.black54,
            ),
            textScaleFactor: 1.5,
          ),
        ),
        Divider(
          height: 2.0,
          color: Colors.blue,
          endIndent: 16.0,
          indent: 16.0,
          thickness: 1.0,
        ),
        Row(
          children: <Widget>[
            Container(
              padding: EdgeInsets.all(8.0),
              child: CircleAvatar(
                backgroundColor: Colors.blue,
                radius: 25.0,
                child: CircleAvatar(
                  backgroundImage: AssetImage('assets/logo.png'),
                  radius: 24.0,
                ),
              ),
            ),
            Expanded(
              child: Text(
                'replied:',
                textScaleFactor: 1.5,
                style: TextStyle(
                  color: Colors.blue,
                ),
              ),
            ),
            Container(
              padding: EdgeInsets.all(16.0),
              child: Text(
                DateTime.now()
                        .difference(DateTime.fromMicrosecondsSinceEpoch(
                            int.parse(tweetDoc.replyTimestamp.date.numberLong) *
                                1000))
                        .inDays
                        .toString() +
                    'd',
                style: TextStyle(color: Colors.grey),
              ),
            ),
          ],
        ),
        Container(
          alignment: Alignment.topLeft,
          padding: EdgeInsets.fromLTRB(8.0, 0, 8.0, 8.0),
          child: Text(
            utf8.decode(tweetDoc.reply.toString().codeUnits),
            style: TextStyle(
              fontStyle: FontStyle.italic,
              fontWeight: FontWeight.w900,
              color: Colors.black54,
            ),
            textScaleFactor: 1.5,
          ),
        ),
        Row(mainAxisAlignment: MainAxisAlignment.end, children: <Widget>[
          FloatingActionButton(
            elevation: 8.0,
            mini: true,
            heroTag: tweetDoc.iId.oid,
            backgroundColor: (tweetDoc.type.compareTo('emergency') == 0)
                ? Colors.deepOrangeAccent[200]
                : Colors.blue,
            tooltip: (tweetDoc.type.compareTo('emergency') == 0)
                ? 'Emergency'
                : 'Feedback',
            onPressed: () {},
            focusColor: (tweetDoc.type.compareTo('emergency') == 0)
                ? Colors.deepOrangeAccent[200]
                : Colors.blue,
            child: Icon(
              (tweetDoc.type.compareTo('emergency') == 0)
                  ? CustomIcons.emergency
                  : CustomIcons.feedback,
              color: Colors.white,
            ),
          ),
        ]),
      ],
    ),
  );
}

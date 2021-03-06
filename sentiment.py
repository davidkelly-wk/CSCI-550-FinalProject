from nltk.corpus import twitter_samples
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections

import tweepy as tw
import nltk
from nltk.corpus import stopwords
import re
import networkx
from textblob import TextBlob

class Sentiment:
    def __init__(self):
        pass

    def score_text(self, tweet_text_string):
        no_url_string = self.remove_url(tweet_text_string)
        sentiment_object = TextBlob(no_url_string)
        score = sentiment_object.polarity
        print(no_url_string)
        print(score)
        return score



    def remove_url(self, txt):
        """Replace URLs found in a text string with nothing
        (i.e. it will remove the URL from the string).
#
        Parameters
        ----------
        txt : string
            A text string that you want to parse and remove urls.
#
        Returns
        -------
        The same txt string with url's removed.
        """
#
        # print('Original', txt)
        return " ".join(re.sub(r'http\S+', '', txt).split())

        # return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())
#
#
# tweets = '{"created_at":"Sat Nov 07 21:37:56 +0000 2020","id":1325190777765425152,"id_str":"1325190777765425152","text":"RT @iam_icaro: happy happy glad thanks :), 2020 t\u00e1 cravado na mem\u00f3ria \ud83e\udd7a https:\/\/t.co\/xlShyDSswv","source":"\u003ca href=\"https:\/\/mobile.twitter.com\" rel=\"nofollow\"\u003eTwitter Web App\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":4777427373,"id_str":"4777427373","name":"Kylo \ud83c\udf7a\ud83e\uddd9\u200d\u2642\ufe0f\ud83d\udc7b\ud83c\udf6b\ud83e\udd98","screen_name":"f_kylo","location":null,"url":null,"description":null,"translator_type":"none","protected":false,"verified":false,"followers_count":767,"friends_count":645,"listed_count":0,"favourites_count":72269,"statuses_count":22817,"created_at":"Mon Jan 11 20:28:59 +0000 2016","utc_offset":null,"time_zone":null,"geo_enabled":false,"lang":null,"contributors_enabled":false,"is_translator":false,"profile_background_color":"F5F8FA","profile_background_image_url":"","profile_background_image_url_https":"","profile_background_tile":false,"profile_link_color":"1DA1F2","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/1312932135414697984\/GbQmlQ6l_normal.jpg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/1312932135414697984\/GbQmlQ6l_normal.jpg","profile_banner_url":"https:\/\/pbs.twimg.com\/profile_banners\/4777427373\/1601601161","default_profile":true,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"retweeted_status":{"created_at":"Sat Nov 07 21:31:15 +0000 2020","id":1325189093228244995,"id_str":"1325189093228244995","text":"Sinceramente eu nunca vou me esquecer disso, 2020 t\u00e1 cravado na mem\u00f3ria \ud83e\udd7a https:\/\/t.co\/xlShyDSswv","source":"\u003ca href=\"http:\/\/twitter.com\/download\/iphone\" rel=\"nofollow\"\u003eTwitter for iPhone\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":3052551550,"id_str":"3052551550","name":"\u00cdcaro","screen_name":"iam_icaro","location":"911 \ud83d\udea8","url":null,"description":"fan account","translator_type":"none","protected":false,"verified":false,"followers_count":1607,"friends_count":960,"listed_count":4,"favourites_count":19283,"statuses_count":15021,"created_at":"Sun Feb 22 11:51:04 +0000 2015","utc_offset":null,"time_zone":null,"geo_enabled":true,"lang":null,"contributors_enabled":false,"is_translator":false,"profile_background_color":"C0DEED","profile_background_image_url":"http:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png","profile_background_image_url_https":"https:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png","profile_background_tile":false,"profile_link_color":"1DA1F2","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/1325048924957237248\/0WEMX0rn_normal.jpg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/1325048924957237248\/0WEMX0rn_normal.jpg","profile_banner_url":"https:\/\/pbs.twimg.com\/profile_banners\/3052551550\/1604413187","default_profile":true,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"is_quote_status":false,"quote_count":2,"reply_count":3,"retweet_count":3,"favorite_count":16,"entities":{"hashtags":[],"urls":[],"user_mentions":[],"symbols":[],"media":[{"id":1264198963898572806,"id_str":"1264198963898572806","indices":[74,97],"additional_media_info":{"monetizable":false},"media_url":"http:\/\/pbs.twimg.com\/ext_tw_video_thumb\/1264198963898572806\/pu\/img\/OhQ0QQmWRM2Pv2Mc.jpg","media_url_https":"https:\/\/pbs.twimg.com\/ext_tw_video_thumb\/1264198963898572806\/pu\/img\/OhQ0QQmWRM2Pv2Mc.jpg","url":"https:\/\/t.co\/xlShyDSswv","display_url":"pic.twitter.com\/xlShyDSswv","expanded_url":"https:\/\/twitter.com\/antonizeior\/status\/1264200060402913280\/video\/1","type":"photo","sizes":{"medium":{"w":640,"h":640,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"},"large":{"w":640,"h":640,"resize":"fit"},"small":{"w":640,"h":640,"resize":"fit"}},"source_status_id":1264200060402913280,"source_status_id_str":"1264200060402913280","source_user_id":1248541469213851648,"source_user_id_str":"1248541469213851648"}]},"extended_entities":{"media":[{"id":1264198963898572806,"id_str":"1264198963898572806","indices":[74,97],"additional_media_info":{"monetizable":false},"media_url":"http:\/\/pbs.twimg.com\/ext_tw_video_thumb\/1264198963898572806\/pu\/img\/OhQ0QQmWRM2Pv2Mc.jpg","media_url_https":"https:\/\/pbs.twimg.com\/ext_tw_video_thumb\/1264198963898572806\/pu\/img\/OhQ0QQmWRM2Pv2Mc.jpg","url":"https:\/\/t.co\/xlShyDSswv","display_url":"pic.twitter.com\/xlShyDSswv","expanded_url":"https:\/\/twitter.com\/antonizeior\/status\/1264200060402913280\/video\/1","type":"video","video_info":{"aspect_ratio":[1,1],"duration_millis":37808,"variants":[{"bitrate":832000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/1264198963898572806\/pu\/vid\/480x480\/YjVcYpVjlnxaeFDt.mp4?tag=10"},{"bitrate":1280000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/1264198963898572806\/pu\/vid\/640x640\/jbOZS2_sfs_2IV2n.mp4?tag=10"},{"bitrate":432000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/1264198963898572806\/pu\/vid\/320x320\/WXLNmKxdTvT81dJ1.mp4?tag=10"},{"content_type":"application\/x-mpegURL","url":"https:\/\/video.twimg.com\/ext_tw_video\/1264198963898572806\/pu\/pl\/ABhpKdccsoOiWBJq.m3u8?tag=10"}]},"sizes":{"medium":{"w":640,"h":640,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"},"large":{"w":640,"h":640,"resize":"fit"},"small":{"w":640,"h":640,"resize":"fit"}},"source_status_id":1264200060402913280,"source_status_id_str":"1264200060402913280","source_user_id":1248541469213851648,"source_user_id_str":"1248541469213851648"}]},"favorited":false,"retweeted":false,"possibly_sensitive":false,"filter_level":"low","lang":"pt"},"is_quote_status":false,"quote_count":0,"reply_count":0,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"urls":[],"user_mentions":[{"screen_name":"iam_icaro","name":"\u00cdcaro","id":3052551550,"id_str":"3052551550","indices":[3,13]}],"symbols":[],"media":[{"id":1264198963898572806,"id_str":"1264198963898572806","indices":[89,112],"additional_media_info":{"monetizable":false},"media_url":"http:\/\/pbs.twimg.com\/ext_tw_video_thumb\/1264198963898572806\/pu\/img\/OhQ0QQmWRM2Pv2Mc.jpg","media_url_https":"https:\/\/pbs.twimg.com\/ext_tw_video_thumb\/1264198963898572806\/pu\/img\/OhQ0QQmWRM2Pv2Mc.jpg","url":"https:\/\/t.co\/xlShyDSswv","display_url":"pic.twitter.com\/xlShyDSswv","expanded_url":"https:\/\/twitter.com\/antonizeior\/status\/1264200060402913280\/video\/1","type":"photo","sizes":{"medium":{"w":640,"h":640,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"},"large":{"w":640,"h":640,"resize":"fit"},"small":{"w":640,"h":640,"resize":"fit"}},"source_status_id":1264200060402913280,"source_status_id_str":"1264200060402913280","source_user_id":1248541469213851648,"source_user_id_str":"1248541469213851648"}]},"extended_entities":{"media":[{"id":1264198963898572806,"id_str":"1264198963898572806","indices":[89,112],"additional_media_info":{"monetizable":false},"media_url":"http:\/\/pbs.twimg.com\/ext_tw_video_thumb\/1264198963898572806\/pu\/img\/OhQ0QQmWRM2Pv2Mc.jpg","media_url_https":"https:\/\/pbs.twimg.com\/ext_tw_video_thumb\/1264198963898572806\/pu\/img\/OhQ0QQmWRM2Pv2Mc.jpg","url":"https:\/\/t.co\/xlShyDSswv","display_url":"pic.twitter.com\/xlShyDSswv","expanded_url":"https:\/\/twitter.com\/antonizeior\/status\/1264200060402913280\/video\/1","type":"video","video_info":{"aspect_ratio":[1,1],"duration_millis":37808,"variants":[{"bitrate":832000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/1264198963898572806\/pu\/vid\/480x480\/YjVcYpVjlnxaeFDt.mp4?tag=10"},{"bitrate":1280000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/1264198963898572806\/pu\/vid\/640x640\/jbOZS2_sfs_2IV2n.mp4?tag=10"},{"bitrate":432000,"content_type":"video\/mp4","url":"https:\/\/video.twimg.com\/ext_tw_video\/1264198963898572806\/pu\/vid\/320x320\/WXLNmKxdTvT81dJ1.mp4?tag=10"},{"content_type":"application\/x-mpegURL","url":"https:\/\/video.twimg.com\/ext_tw_video\/1264198963898572806\/pu\/pl\/ABhpKdccsoOiWBJq.m3u8?tag=10"}]},"sizes":{"medium":{"w":640,"h":640,"resize":"fit"},"thumb":{"w":150,"h":150,"resize":"crop"},"large":{"w":640,"h":640,"resize":"fit"},"small":{"w":640,"h":640,"resize":"fit"}},"source_status_id":1264200060402913280,"source_status_id_str":"1264200060402913280","source_user_id":1248541469213851648,"source_user_id_str":"1248541469213851648"}]},"favorited":false,"retweeted":false,"possibly_sensitive":false,"filter_level":"low","lang":"pt","timestamp_ms":"1604785076930"}'
#
#
# tweets_no_urls = [remove_url(tweets)]







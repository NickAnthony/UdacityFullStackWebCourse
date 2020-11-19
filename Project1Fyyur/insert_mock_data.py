import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import datetime

from app import db, Venue, Artist, Show

def venue_or_artist_exists(existing_rows, name):
    for existing_row in existing_rows:
        if existing_row.name == name:
            return True
    return False

# Venue data:
venue_data = [{
       "id": 1,
       "name": "The Musical Hop",
       "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
       "address": "1015 Folsom Street",
       "city": "San Francisco",
       "state": "CA",
       "phone": "123-123-1234",
       "website": "https://www.themusicalhop.com",
       "facebook_link": "https://www.facebook.com/TheMusicalHop",
       "seeking_talent": True,
       "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
       "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
       "past_shows": [{
         "artist_id": 4,
         "artist_name": "Guns N Petals",
         "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
         "start_time": "2019-05-21T21:30:00.000Z"
       }],
       "upcoming_shows": [],
       "past_shows_count": 1,
       "upcoming_shows_count": 0,
     },{
       "name": "The Dueling Pianos Bar",
       "genres": ["Classical", "R&B", "Hip-Hop"],
       "address": "335 Delancey Street",
       "city": "New York",
       "state": "NY",
       "phone": "914-003-1132",
       "website": "https://www.theduelingpianos.com",
       "facebook_link": "https://www.facebook.com/theduelingpianos",
       "seeking_talent": False,
       "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
       "past_shows": [],
       "upcoming_shows": [],
       "past_shows_count": 0,
       "upcoming_shows_count": 0,
     },{
       "name": "Park Square Live Music & Coffee",
       "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
       "address": "34 Whiskey Moore Ave",
       "city": "San Francisco",
       "state": "CA",
       "phone": "415-000-1234",
       "website": "https://www.parksquarelivemusicandcoffee.com",
       "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
       "seeking_talent": False,
       "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
       "past_shows": [{
         "artist_id": 5,
         "artist_name": "Matt Quevedo",
         "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
         "start_time": "2019-06-15T23:00:00.000Z"
       }],
       "upcoming_shows": [{
         "artist_id": 6,
         "artist_name": "The Wild Sax Band",
         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
         "start_time": "2035-04-01T20:00:00.000Z"
       }, {
         "artist_id": 6,
         "artist_name": "The Wild Sax Band",
         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
         "start_time": "2035-04-08T20:00:00.000Z"
       }, {
         "artist_id": 6,
         "artist_name": "The Wild Sax Band",
         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
         "start_time": "2035-04-15T20:00:00.000Z"
       }],
       "past_shows_count": 1,
       "upcoming_shows_count": 1,
     }]
existing_venues = Venue.query.all()
for data in venue_data:
    if venue_or_artist_exists(existing_venues, data["name"]):
        continue;
    new_venue = Venue(
       name=data["name"],
       genres=data["genres"],
       address=data["address"],
       city=data["city"],
       state=data["state"],
       phone=data["phone"],
       website=data["website"],
       facebook_link=data["facebook_link"],
       seeking_talent=data["seeking_talent"] if
                      ("seeking_talent" in data) else None,
       seeking_description=data["seeking_description"] if
                           ("seeking_description" in data) else None,
       image_link=data["image_link"]
    )
    db.session.add(new_venue)
db.session.commit()

artist_data = [{
          "name": "Guns N Petals",
          "genres": ["Rock n Roll"],
          "city": "San Francisco",
          "state": "CA",
          "phone": "326-123-5000",
          "website": "https://www.gunsnpetalsband.com",
          "facebook_link": "https://www.facebook.com/GunsNPetals",
          "seeking_venue": True,
          "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
          "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
          "past_shows": [{
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "start_time": "2019-05-21T21:30:00.000Z"
          }],
          "upcoming_shows": [],
          "past_shows_count": 1,
          "upcoming_shows_count": 0,
        },{
          "name": "Matt Quevedo",
          "genres": ["Jazz"],
          "city": "New York",
          "state": "NY",
          "phone": "300-400-5000",
          "facebook_link": "https://www.facebook.com/mattquevedo923251523",
          "seeking_venue": False,
          "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
          "past_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2019-06-15T23:00:00.000Z"
          }],
          "upcoming_shows": [],
          "past_shows_count": 1,
          "upcoming_shows_count": 0,
        },{
          "name": "The Wild Sax Band",
          "genres": ["Jazz", "Classical"],
          "city": "San Francisco",
          "state": "CA",
          "phone": "432-325-5432",
          "seeking_venue": False,
          "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
          "past_shows": [],
          "upcoming_shows": [{
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-01T20:00:00.000Z"
          }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-08T20:00:00.000Z"
          }, {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "start_time": "2035-04-15T20:00:00.000Z"
          }],
          "past_shows_count": 0,
          "upcoming_shows_count": 3,
        }]
existing_artists = Artist.query.all()
for data in artist_data:
    if venue_or_artist_exists(existing_artists, data["name"]):
        continue;
    new_artist = Artist(
       name=data["name"],
       genres=data["genres"],
       city=data["city"],
       state=data["state"],
       phone=data["phone"],
       website=data["website"] if ("website" in data) else None,
       facebook_link=data["facebook_link"] if "facebook_link" in data else None,
       seeking_venue=data["seeking_venue"] if
                      ("seeking_venue" in data) else None,
       seeking_description=data["seeking_description"] if
                           ("seeking_description" in data) else None,
       image_link=data["image_link"]
    )
    db.session.add(new_artist)
db.session.commit()

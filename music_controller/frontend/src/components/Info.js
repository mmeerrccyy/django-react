import React, { Component, useState, useEffect } from "react";
import { Grid, IconButton, Typography, Button } from "@material-ui/core";
import NavigateBeforeIcon from "@material-ui/icons/NavigateBefore";
import NavigateNextIcon from "@material-ui/icons/NavigateNext";
import { Link } from "react-router-dom";

export default function Info(props) {
  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          What is House Party?
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <Typography variant="body1">
        <p>{"Hello! My name is Taras. It is my first Django REST and React Project."}</p>
        <p>{"This is site, where you can listen music in room with your friends."}</p>
        <p>{"Warning! Host must have Spotify Premium for music control."}</p>
        <p>{"Thanks for wathicng my project! <3"}</p>
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="secondary" variant="contained" to="/" component={Link}>
          Back
        </Button>
      </Grid>
    </Grid>
  );
}

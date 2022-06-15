package com.ggar.streamlinkplus.api;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class StreamApiDelegateImpl implements StreamApiDelegate {
    @Override
    public ResponseEntity<Boolean> getStreamHealthCheck() {
        return new ResponseEntity<Boolean>(true, HttpStatus.OK);
    }
}

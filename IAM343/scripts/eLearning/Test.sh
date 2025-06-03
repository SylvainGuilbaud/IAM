## run the curl to get an entry in IAM and then read input with a 5 second timeout
## repeat if no entry or entry is not 'STOP'
## quit the loop if 'STOP' is entered within the read timeout
 
#!/bin/bash
 
loopCount=0
while [ : ]
do
        ## Student is doing 10 calls per loop (~100 calls per minute)
        curl -i -X GET --url http://10.0.0.1:8000/coffeemakers -u "student:demo3232" > /dev/null
        curl -i -X GET --url http://10.0.0.1:8000/coffeemakers -u "student:demo3232" > /dev/null
        curl -i -X GET --url http://10.0.0.1:8000/coffeemakers -u "student:demo3232" > /dev/null
        curl -i -X GET --url http://10.0.0.1:8000/coffeemakers -u "student:demo3232" > /dev/null
        curl -i -X GET --url http://10.0.0.1:8000/coffeemakers -u "student:demo3232" > /dev/null
        curl -i -X GET --url http://10.0.0.1:8000/coffeemakers -u "student:demo3232" > /dev/null
        curl -i -X GET --url http://10.0.0.1:8000/coffeemakers -u "student:demo3232" > /dev/null
        curl -i -X GET --url http://10.0.0.1:8000/coffeemakers -u "student:demo3232" > /dev/null
        curl -i -X GET --url http://10.0.0.1:8000/coffeemakers -u "student:WrongPassword" > /dev/null
        curl -i -X GET --url http://10.0.0.1:8000/BADendpoint -u "student:demo3232" > /dev/null
        let "loopCount++"
        echo "Loop number: "$loopCount"     Enter 'STOP' to stop the loop "
        read -t 5
        STATUS=$?
        if test $STATUS -eq 0; then
                if [ $REPLY = "STOP" ]; then
                                break
                fi
        fi
done
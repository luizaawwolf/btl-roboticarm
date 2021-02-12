#include <BraccioV2.h>

#include "BraccioV2.h"
Braccio arm;


//Set these values from the min/max gripper joint values below.
#define GRIPPER_CLOSED 85
#define GRIPPER_OPENED 20

void setup() {
  Serial.begin(9600);
  Serial.println("Initializing... Please Wait");//Start of initialization, see note below regarding begin method.

  //Calibration values from running calibration program
  arm.setJointCenter(BASE_ROT, 120);
  arm.setJointMin(BASE_ROT, 0);
  arm.setJointMax(BASE_ROT, 180);
  
  
  arm.setJointCenter(SHOULDER, 98);
  arm.setJointMin(SHOULDER, 0);
  arm.setJointMax(SHOULDER, 180);
  
  
  arm.setJointCenter(ELBOW, 93);
  arm.setJointMin(ELBOW, 7);
  arm.setJointMax(ELBOW, 180);
  
  arm.setJointCenter(WRIST, 98);
  arm.setJointMin(WRIST, 12);
  arm.setJointMax(WRIST, 180);
  
  
  arm.setJointCenter(WRIST_ROT, 90);
  arm.setJointMin(WRIST_ROT, 0);
  arm.setJointMax(WRIST_ROT, 180);
  
  
  arm.setJointCenter(GRIPPER, 40);
  arm.setJointMin(GRIPPER, 15);
  arm.setJointMax(GRIPPER, 80);

  //Set max/min values for joints as needed. Default is min: 0, max: 180
  //The only two joints that should need this set are gripper and shoulder.
  arm.setJointMax(GRIPPER, 100);//Gripper closed, can go further, but risks damage to servos
  arm.setJointMin(GRIPPER, 15);//Gripper open, can't open further

  arm.begin(true);// Start to default vertical position.
  //to initialize the power circuitry.
  Serial.println("Initialization Complete");
}


//int[] random_arm_position(){
//  int theta_shoulder = int(random(0,180)); // #alternatively, this could be (50, 140), the other values can be any random from (0, 180) and it shouldn't hit
//  int theta_elbow = elbow_angle(theta_shoulder);
//  int theta_wrist = int(random(0,180));
//  return theta_shoulder, theta_elbow, theta_wrist;
//}

void random_arm_position(){
  int theta_base = int(random(0,180));
  int theta_shoulder = int(random(0,180));
  int theta_elbow = elbow_angle(theta_shoulder);
  int theta_wrist = int(random(0,180));
  arm.setOneAbsolute(BASE_ROT, theta_base);
  arm.safeDelay(1000);
  if( theta_shoulder >= 140 or theta_shoulder <= 40 ){
    arm.setOneAbsolute(ELBOW, 90);
    arm.safeDelay(1000);
    arm.setOneAbsolute(WRIST, 90);
    arm.safeDelay(1000);
    //resetting elbow and wrist so they don't hit when shoulder is sent to new position
  }
  Serial.println(theta_shoulder);
  arm.setOneAbsolute(SHOULDER, theta_shoulder);
  arm.safeDelay(1000);
  Serial.println(theta_elbow);
  arm.setOneAbsolute(ELBOW, theta_elbow);
  arm.safeDelay(1000);
  Serial.println(theta_wrist);
  arm.setOneAbsolute(WRIST, theta_wrist);
  arm.safeDelay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available() < 1);
      char c = Serial.read();
  if( c == 'b' ){ //moving the base
      int desiredPosition = Serial.parseInt();
      arm.setOneAbsolute(BASE_ROT, desiredPosition);
      arm.safeDelay(3000);
  } else if ( c == 's' ){
    // moving the shoulder
      int desiredPosition = Serial.parseInt();
      arm.setOneAbsolute(SHOULDER, desiredPosition);
      arm.safeDelay(3000);
  } else if ( c == 'e' ){
    // moving the elbow
      int desiredPosition = Serial.parseInt();
      arm.setOneAbsolute(ELBOW, desiredPosition);
      arm.safeDelay(3000);
  } else if ( c == 'w' ){
    // moving the wrist
      int desiredPosition = Serial.parseInt();
      arm.setOneAbsolute(WRIST, desiredPosition);
      arm.safeDelay(3000);
  } else if ( c == 'r' ) {
    for( int i = 0; i < 40; i++ ){
      random_arm_position();
      arm.safeDelay(1000);
    }
  }

//  while(Serial.available() < 1);
//      char c = Serial.read();
//
//  int v = 180;
//  arm.setOneAbsolute(SHOULDER, v);
//  arm.safeDelay(3000);
//  for( int i = 90; i < 120; i ++ ){
//    arm.setOneAbsolute(ELBOW, i);
//    arm.safeDelay(1000);
//    if( c == 'b' ){ //break
//      break;
//    }
//  }

}

// THIS DOESN'T TAKE INTO ACCOUNT A FULL RANGE OF POSSIBLE VALUES
float coeffs_elbow_g140[] = { 2.26881720e-02, -8.59107527e+00,  9.45229032e+02};
float coeffs_elbow_l40[] = {-3.72727273e-02  ,5.69090909e-01,  6.02181818e+01};

int elbow_angle(int shoulder_angle){
  int maximum_elbow_theta = 180 ;
  int minimum_elbow_theta = 0;
  if ( shoulder_angle >= 140 ){
        maximum_elbow_theta = coeffs_elbow_g140[0]*(pow(shoulder_angle,2)) + coeffs_elbow_g140[1]*shoulder_angle + coeffs_elbow_g140[2] ;
        minimum_elbow_theta = 0; //find relationship
  } else if ( shoulder_angle <= 40) {
        maximum_elbow_theta =  180;
        minimum_elbow_theta = coeffs_elbow_l40[0]*(pow(shoulder_angle,2)) + coeffs_elbow_l40[1]*shoulder_angle + coeffs_elbow_l40[2];; //find relationship
  }
   
  return int(random(minimum_elbow_theta, int(maximum_elbow_theta)));
  
}

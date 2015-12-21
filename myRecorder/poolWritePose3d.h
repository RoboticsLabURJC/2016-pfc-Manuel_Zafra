#ifndef poolWritePose3d_H_
#define poolWritePose3d_H_

#include <pthread.h>
#include <boost/thread/thread.hpp>
#include <stdio.h>
#include <time.h>
#include <jderobot/pose3d.h>
#include <fstream>



namespace recorder{

struct pose3d{
	float x;
	float y;
	float z;
	float q0;
	float q1;
	float q2;
	float q3;
};


class poolWritePose3d {
public:
	poolWritePose3d(jderobot::Pose3DPrx p3drx, int freq, int poolSize, int encoderID);
	virtual ~poolWritePose3d();
	bool getActive();
	//void produceImage(cv::Mat image, long long int it);
	void consumer_thread();
	void producer_thread(struct timeval inicio);


private:
	pthread_mutex_t mutex;
	std::vector<pose3d> encoders;
	std::vector<long long int> its;
	int poolSize;
	int encoderID;
	bool active;
	struct timeval lastTime;
	int freq;
	float cycle;
	jderobot::Pose3DPrx p3drx;
	std::ofstream outfile;


	//threads

};
} //NAMESPACE
#endif /* poolWritePose3d_H_ */
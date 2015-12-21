#include "poolWritePose3d.h"

namespace recorder{


poolWritePose3d::poolWritePose3d(jderobot::Pose3DPrx p3drx, int freq, int poolSize, int encoderID) {
	// TODO Auto-generated constructor stub
	pthread_mutex_init(&(this->mutex), NULL);
	this->poolSize=poolSize;
	this->encoderID=encoderID;
	this->active=true;
	this->p3drx=p3drx;
	this->freq=freq;
	std::stringstream filePath;
	filePath << "data/pose3d/pose3d" << this->encoderID << "/pose3dData.jde";
	this->cycle = 1000.0/freq;
	this->outfile.open(filePath.str().c_str());
	gettimeofday(&lastTime,NULL);
}

poolWritePose3d::~poolWritePose3d() {
	this->outfile.close();
	// TODO Auto-generated destructor stub
}

bool poolWritePose3d::getActive(){
	return this->active;
}

void poolWritePose3d::consumer_thread(){
//	while(this->active){

		pthread_mutex_lock(&(this->mutex));
		if (this->encoders.size()>0){
			//std::cout << " camara: " << cameraID <<  this->images.size()  << std::endl;

			recorder::pose3d data2Save;
			data2Save = this->encoders[0];
			std::cout <<"b " <<data2Save.x<< "\n";
			std::cout <<"b " <<data2Save.y<< "\n";
			std::cout <<"b " <<data2Save.z<< "\n";
			std::cout <<"b " <<data2Save.q0<< "\n";
			std::cout <<"b " <<data2Save.q1<< "\n";
			std::cout <<"b " <<data2Save.q2<< "\n";
			std::cout <<"b " <<data2Save.q3<< "\n";
			this->encoders.erase(this->encoders.begin());
			long long int relative;
			relative=*(this->its.begin());
			this->its.erase(this->its.begin());
			pthread_mutex_unlock(&(this->mutex));


			std::stringstream idString;//create a stringstream
			idString << this->encoderID;//add number to the stream
			std::stringstream relativeString;//create a stringstream
			relativeString << relative;//add number to the stream


			std::string Path="data/pose3d/pose3d" + idString.str() + "/" + relativeString.str();
			std::ofstream outfileBinary(Path.c_str(), std::ios::out | std::ios::binary);
			outfileBinary.write((const char *)&data2Save, sizeof(recorder::pose3d));
			outfileBinary.close();

			//this->outfile << relative  << " " << data2Save.x   << " " << data2Save.y << " " << data2Save.z << " " << data2Save.q0 << " " << data2Save.q1 << " " << data2Save.q2 << " " << data2Save.q3 << std::endl;
			this->outfile << relative     << " ";
			this->outfile << data2Save.x  << " ";
			this->outfile << data2Save.y  << " ";
			this->outfile << data2Save.z  << " ";
			this->outfile << data2Save.q0 << " ";
			this->outfile << data2Save.q1 << " ";
			this->outfile << data2Save.q2 << " ";
			this->outfile << data2Save.q3 << std::endl;
		}
		else
			pthread_mutex_unlock(&(this->mutex));
		usleep(1000);


//	}
}

void poolWritePose3d::producer_thread(struct timeval inicio){
	//std::cout << "productor entro" << std::endl;
//	while(this->active){


		jderobot::Pose3DDataPtr dataPtr=this->p3drx->getPose3DData();
		std::cout << "Producer \t" << dataPtr << "\n";
		recorder::pose3d data;
		data.x=dataPtr->x;
		data.y=dataPtr->y;
		data.z=dataPtr->z;
		data.q0=dataPtr->q0;
		data.q1=dataPtr->q1;
		data.q2=dataPtr->q2;
		data.q3=dataPtr->q3;
		std::cout <<"a " <<data.x<< "\n";
		std::cout <<"a " <<data.y<< "\n";
		std::cout <<"a " <<data.z<< "\n";
		std::cout <<"a " <<data.q0<< "\n";
		std::cout <<"a " <<data.q1<< "\n";
		std::cout <<"a " <<data.q2<< "\n";
		std::cout <<"a " <<data.q3<< "\n";

		struct timeval now;
		gettimeofday(&now,NULL);
		long long int relative;
		relative=((now.tv_sec*1000000+now.tv_usec) - (inicio.tv_sec*1000000+inicio.tv_usec))/1000;
		pthread_mutex_lock(&(this->mutex));
		while (this->encoders.size() > this->poolSize){
			pthread_mutex_unlock(&(this->mutex));
			usleep(100);
			pthread_mutex_lock(&(this->mutex));
		}
		this->encoders.push_back(data);
		this->its.push_back(relative);
		pthread_mutex_unlock(&(this->mutex));
		gettimeofday(&now,NULL);

		long long int totalNow=now.tv_sec*1000000+now.tv_usec;
		long long int totalLast=lastTime.tv_sec*1000000+lastTime.tv_usec;

		float sleepTime =this->cycle - (totalNow-totalLast)/1000.;

		//std::cout << "productor: " << this->cameraID << ", sleep: " << sleepTime << std::endl;
		if(sleepTime < 0 )
			sleepTime = 0;
		usleep(sleepTime*1000);
		gettimeofday(&lastTime,NULL);
		//std::cout << "productor salgo" << std::endl;
//	}
}


} //namespace

#include <stdio.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#define MAXLINE 4096
#define Server_port 8080
#define SockA struct sockaddr

long long factorial(int x){
    
    long long fact = 1 ;
    while (x!=0)
    {
        fact=fact*x ;
        x-- ;

    }

return fact;
    
}
FILE *file_pointer;

void func(int connfd)
{   
    // declaring file pointer
    
    // opening file in write mode
    file_pointer = fopen("file2.text","w");
    int recived;
    int i =1;
    while(i<=10){
        read(connfd, &recived, sizeof(recived));
        printf("Msg from client: %d\n", recived);
        long long ans = factorial((long long)recived);
        fprintf(file_pointer,"Factorial of received( %d) no. : %lld\n\n",recived,ans);
        printf("send to client factorial:%lld of received data(( %d))\n",ans,recived);
        write(connfd,&ans,sizeof(ans));
        i++;
        printf("\n");
    }
    
    exit(0);
}


int main(){
	int sock_open , confirToConnect, len;
	struct sockaddr_in servaddrPort, cli;
	
	sock_open = socket(AF_INET, SOCK_STREAM, 0);
	//checking socket is made or not 
	if (sock_open == -1) {
        printf("socket  failed...\n");
        exit(0);
    }
    else
        printf("Socket successfully created..\n");
	// binding to port (TCp)
	servaddrPort.sin_family = AF_INET;
    servaddrPort.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddrPort.sin_port = htons(Server_port);

	// assihn address to socket bind()
	int b_status = bind(sock_open,(SockA*)&servaddrPort ,sizeof(servaddrPort));
	//verification
	if (b_status !=0){
		printf("socket bind failed...\n");
        exit(0);
	}
	else
        printf("Socket successfully binded..\n");

	// Listen and verifcation
	int l_status= listen(sock_open, 20);
	if (l_status != 0) {
        printf("Listen failed...\n");
        exit(0);
    }
    else
        printf("Server listening..\n");
    
	len = sizeof(cli); // taking size

    while(1){
        pid_t child;
    
	// Accept the data packet from client and verification
    confirToConnect = accept(sock_open, (SockA*)&cli, &len);
    if (confirToConnect < 0) {
        printf("server accept failed...\n");
        exit(0);
    }
    else
        printf("server accept the client...\n");
    
    if((child = fork()) ==0){
        // client and server hansake data
        close(sock_open);
        func(confirToConnect);
    }
    // close(sock_open);
    close(confirToConnect);
    }
	return 0;
}


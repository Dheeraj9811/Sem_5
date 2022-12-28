
#include <stdio.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#define MAXLINE 4096
#define Server_port 8080
#define SockA struct sockaddr



long long int factorial(int x){
    
    long long int fact = 1 ;
    while (x!=0)
    {
        fact=fact*x ;
        x-- ;

    }
    return fact;
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

	// Accept the data packet from client and verification
    confirToConnect = accept(sock_open, (SockA*)&cli, &len);
	if (confirToConnect < 0) {
        printf("server accept failed...\n");
        exit(0);
    }
    else
        printf("server accept the client...\n");
    // client and server hansake data
    func(confirToConnect);

    close(sock_open);

	return 0;
}
void func(int connfd)
{
    char buff[MAXLINE];
    int n;
    // infinite loop for chat
    for (;;) {
        bzero(buff, MAXLINE);
   
        // read the message from client and copy it in buffer
        int x = read(connfd, buff, sizeof(buff));
        if(x==0)break;
        // print buffer which contains the client contents
        int req = atoi(buff);

        bzero(buff, MAXLINE);
        // n = 0;
        // // copy server message in the buffer
        // while ((buff[n++] = getchar()) != '\n')
        //     ;
        long long int ans  = factorial(req);
        bzero(buff,sizeof(buff));
        sprintf(buff,"%lld",ans);
        // and send that buffer to client
        write(connfd, buff, sizeof(buff));
   
        
    }
    
    
}

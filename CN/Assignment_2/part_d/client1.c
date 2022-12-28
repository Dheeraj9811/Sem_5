#include <arpa/inet.h> // inet_addr()
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h> // bzero()
#include <sys/socket.h>
#include <unistd.h> // read(), write(), close()
#define MAX 4096
#define PORT 8080
#define SA struct sockaddr
#include <pthread.h>
void func(int sockfd)
{   
    int i =1;
    long long recived;
    while(1){
        printf("sending to server: %d\n",i);
        write(sockfd,&i, sizeof(i));
        read(sockfd,&recived,sizeof(recived));
        printf("from server factorial: %lld\n", recived );
        i++;
        printf("\n");

        if(i> 20){
            break;
        }
    }
   
}
void * Thread_fn(void *arg){
    int sockfd;
    struct sockaddr_in servaddr;
 
    // socket create and verification
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("socket creation failed...\n");
        exit(0);
    }
    else
        printf("Socket successfully created..\n");
    bzero(&servaddr, sizeof(servaddr));
 
    // assign IP, PORT
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(PORT);
 
    // connect the client socket to server socket
    if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr))
        != 0) {
        printf("connection with the server failed...\n");
        exit(0);
    }
    else
        printf("connected to the server..\n");
 
    // function for chat
    func(sockfd);
 
    // close the socket
    close(sockfd);
}
 
int main()
{
    pthread_t thread_arr[10];

    for(int i = 0 ; i<10;i++){
        pthread_create(&thread_arr[i], NULL, Thread_fn, NULL);
        
    }
    for (size_t i = 0; i < 10; i++)
    {
        pthread_join(thread_arr[i], NULL);
    }
    
    return 0;
}


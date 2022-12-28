#include<stdio.h>
#include<netinet/in.h>
#include<unistd.h>
#include<string.h>
#include<errno.h>
#include<poll.h>
#include<arpa/inet.h>
#include<sys/epoll.h>
#include<stdlib.h>
// taken from lecture code of this part
#define DATA_BUFFER 600
#define Max_connect 20
#define Server_port 8080

long long factorial(int x){
    
    long long fact = 1 ;
    while (x!=0)
    {
        fact=fact*x ;
        x-- ;

    }

return fact;
}

int create_tcp_server_socket(){
    struct sockaddr_in saddr;
    int fd, return_value;

    fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (fd == -1){
        printf("socket bind failed......\n\n");
        return -1;
    }
    printf("Socket successfully binded.....\n\n");

    saddr.sin_family = AF_INET;
    saddr.sin_port = htons(Server_port);
    saddr.sin_addr.s_addr = INADDR_ANY;

    return_value = bind(fd, (struct sockaddr *)&saddr, sizeof(struct sockaddr_in));
    if (return_value != 0){
        printf("BINDING FAILED...\n\n");
        close(fd);
        return -1;
    }
    printf("BINDED THE SOCKET...\n\n");

    return_value = listen(fd, 10);
    if (return_value != 0){
        printf("LISTENING FAILED...\n\n");
        close(fd);
        return -1;
    }
    printf("Listing..\n\n");

    return fd;
}

int main(){
    struct sockaddr_in new_addr;
    int server_fd, return_value, i, all_connections[Max_connect], nfds = Max_connect-1, num_open_fds = nfds, useClient = 0;
    socklen_t addrlen;
    struct epoll_event ev, *events;
    int epollfd = epoll_create(20);
    events  = (struct epoll_event* ) calloc(Max_connect,sizeof(struct epoll_event));


    FILE *fp;
    fp = fopen("file3.txt", "w");

    server_fd = create_tcp_server_socket();
    if(server_fd == -1){
        printf("SERVER CREATION FAILED...\n\n");
        return -1;
    }
    printf("SERVER CREATED...\n\n");

    ev.data.fd = server_fd;
    ev.events = EPOLLIN;
    epoll_ctl(epollfd, EPOLL_CTL_ADD, server_fd, &ev);
    while (1){
        return_value = epoll_wait(epollfd,events,11,-1);

        if (return_value >= 0){
            for(int i=0;i<return_value;i++){
                int current_fd = events[i].data.fd;
                if(current_fd == server_fd){
                    int new_fd = accept(server_fd, (struct sockaddr*)&new_addr, &addrlen);
                    if (new_fd >= 0) {
                        printf("ACCEPTED A NEW CONNECTION WITH FILE DESCRIPTOR: %d\n\n", new_fd);
                        //Add new client here
                        struct epoll_event ev_1;
                        ev_1.events = EPOLLIN;
                        ev_1.data.fd = new_fd;
                        epoll_ctl(epollfd, EPOLL_CTL_ADD, new_fd,&ev_1);
                    }
                    else{
                        printf("ACCEPTING FAILED...\n\n");
                    }
                }
                else{
                    int n;
                    int bufSize = read(current_fd, &n, sizeof(int));
                    socklen_t addrsize = sizeof(new_addr);
                    getpeername(current_fd,(struct sockaddr *)&new_addr,(socklen_t*)&addrsize);
                    if (bufSize == -1){
                        printf("Read Error\n");
                        return 0;
                    }
                    else if (bufSize == 0){
                        struct epoll_event ev_2;
                        ev_2.events = EPOLLIN;
                        ev_2.data.fd = current_fd;
                        epoll_ctl(epollfd, EPOLL_CTL_DEL, current_fd,&ev_2);
                        useClient--;
                    }
                    else{
                        printf("FROM CLIENT: %d \n\n", n);
                        long long res = factorial(n);
                        fprintf(fp, "IP: %s, Server_port: %d, FACTORIAL: %lld \n\n", inet_ntoa(new_addr.sin_addr), ntohs(new_addr.sin_port), res);
                        fflush(fp);
                        printf("TO CLIENT: %lld\n\n", res);   
                        write(current_fd, &res, sizeof(res));
                    }

                }
            }
        }
    }

    fclose(fp);
    return 0;
}
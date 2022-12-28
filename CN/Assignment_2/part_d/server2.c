#include<stdio.h>
#include<netinet/in.h>
#include<unistd.h>
#include<string.h>
#include<errno.h>
#include<poll.h>
#include<arpa/inet.h>
// taken from lecture code of this part
#define DATA_BUFFER 5000
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
        printf("SOCKET CREATION FAILED...\n\n");
        return -1;
    }
    printf("CREATED SOCKET...\n\n");

    saddr.sin_family = AF_INET;
    saddr.sin_port = htons(Server_port);
    saddr.sin_addr.s_addr = INADDR_ANY;

    return_value = bind(fd, (struct sockaddr *)&saddr, sizeof(struct sockaddr_in));
    if (return_value != 0){
        printf("socket bind failed...\n\n");
        close(fd);
        return -1;
    }
    printf("Socket successfully binded..\n\n");

    return_value = listen(fd, 10);
    if (return_value != 0){
        printf("Listen failed...\n\n");
        close(fd);
        return -1;
    }
    printf("Listen.\n\n");

    return fd;
}

int main(){
    struct sockaddr_in new_addr;
    int server_fd, return_value, i, n, all_connections[Max_connect], nfds = Max_connect-1, num_open_fds = nfds, useClient = 0;
    socklen_t addrlen;
    struct pollfd *pfds, pollfds[Max_connect];

    FILE *fp;
    fp = fopen("file2.txt", "w+");

    server_fd = create_tcp_server_socket();
    if(server_fd == -1){
        printf("SERVER CREATION FAILED...\n\n");
        return -1;
    }
    printf("SERVER CREATED...\n\n");

    pollfds[0].fd = server_fd;
    pollfds[0].events = POLLIN;

    for(i = 1; i < Max_connect; i++){
        pollfds[i].fd = 0;
        pollfds[i].events = POLLIN;
    }

    while (1){
        return_value = poll(pollfds,20, 5000);

        if (return_value >= 0){
            if (pollfds[0].revents & POLLIN) {

                int new_fd = accept(server_fd, (struct sockaddr*)&new_addr, &addrlen);

                if (new_fd >= 0) {
                    printf("ACCEPTED A NEW CONNECTION WITH FILE DESCRIPTOR: %d\n\n", new_fd);
                    for(i = 1; i < Max_connect; i++){
                        if (pollfds[i].fd == 0){
                            pollfds[i].fd = new_fd;
                            pollfds[i].events = POLLIN;
                            useClient++;
                            break;
                        }
                    }
                }
                else{
                    printf("ACCEPTING FAILED...\n\n");
                }
                return_value--;
                if( !return_value) continue;
            }

            for(i = 1; i < Max_connect; i++){
                if (pollfds[i].fd > 0 && pollfds[i].revents & POLLIN)
                {
                    int bufSize = read(pollfds[i].fd, &n, sizeof(int));
                    if (bufSize == -1){
                        pollfds[i].fd = 0;
                        pollfds[i].events = 0;
                        pollfds[i].revents = 0;
                        useClient--;
                    }
                    else if (bufSize == 0){
                        close(pollfds[i].fd);
                        pollfds[i].fd = 0;
                        pollfds[i].events = 0;
                        pollfds[i].revents = 0;
                        useClient--;
                    }
                    else{
                        printf("FROM CLIENT: %d \n\n", n);
                        long long res = factorial(n);

                        fprintf(fp, "IP: %s, Server_port: %d, FACTORIAL: %lld \n\n", inet_ntoa(new_addr.sin_addr), ntohs(new_addr.sin_port), res);
                        fflush(fp);

                        printf("TO CLIENT: %lld\n\n", res);   

                        write(pollfds[i].fd, &res, sizeof(res));
                        
                    }
                }
            }
        }
    }

    fclose(fp);
    return 0;
}
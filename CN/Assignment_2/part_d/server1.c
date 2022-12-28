#include<stdio.h>
#include<netinet/in.h>
#include<unistd.h>
#include<string.h>
#include<errno.h>
#include<sys/select.h>
#include<arpa/inet.h>

// taken from lecture code of this part

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
    printf("SOCKET CREATED...\n\n");

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
    printf("LISTENING...\n\n");
    return fd;
}


int main(){
    fd_set read_fd_set;
    struct sockaddr_in new_addr;
    int server_fd, new_fd, return_value, i, n, all_connections[Max_connect];
    socklen_t addrlen;

    FILE *fp;
    fp = fopen("file1.txt", "w");

    // CREATING SOCKET - SERVER
    server_fd = create_tcp_server_socket();
    if(server_fd == -1){
        printf("SERVER CREATION FAILED...\n\n");
        return -1;
    }
    printf("SERVER CREATED...\n\n");

    // INITIALIZING ALL THE CONNECTIONS
    for(i = 0; i < Max_connect; i++){
        all_connections[i] = -1;
    }
    all_connections[0] = server_fd;

    while(1){
        FD_ZERO(&read_fd_set);

        //SETTING THE FILE DESCRIPTOR
        for(i=0; i< Max_connect; i++){
            if (all_connections[i] >= 0){
                FD_SET(all_connections[i], &read_fd_set);
            }
        }

        // SELECTING ACTIVE FILE DESCRIPTOR
        return_value = select(FD_SETSIZE, &read_fd_set, NULL, NULL, NULL);

        if(return_value >= 0){
            if(FD_ISSET(server_fd, &read_fd_set)) {
                new_fd = accept(server_fd, (struct sockaddr*)&new_addr, &addrlen);
                if(new_fd >= 0){
                    printf("CONNECTION ACCEPTED ...\n\n");

                    for(i=0 ; i < Max_connect ; i++){
                        if(all_connections[i] < 0){
                            all_connections[i] = new_fd;
                            break;
                        }
                    }
                } else{
                    printf("FAILED ACCEPT ...\n\n");
                }
                return_value--;
                if (!return_value) continue;
            }


            for(i=1; i < Max_connect; i++){
                if((all_connections[i]>0) && (FD_ISSET(all_connections[i], &read_fd_set))){

                    return_value = read(all_connections[i], &n, sizeof(int));
                    if (return_value == 0){
                        printf("CLOSING CONNECTION FOR CLIENT WITH FD: %d\n\n", all_connections[i]);
                        close(all_connections[i]);
                        all_connections[i] = -1;
                    }
                    if (return_value > 0){

                        printf("RECIEVED DATA (LENGTH %d BYTES, fd: %d): %d\n\n", return_value, all_connections[i], n);

                        long long res = factorial(n);

                        fprintf(fp, "IP: %s, Server_port: %d, FACTORIAL: %lld \n\n", inet_ntoa(new_addr.sin_addr), ntohs(new_addr.sin_port), res);
                        fflush(fp);

                        printf("SENT DATA (LENGTH %d BYTES, fd: %d): %lld\n\n", return_value, all_connections[i], res);

                        write(all_connections[i], &res, sizeof(res));
                    }
                    if (return_value == -1){
                        printf("READ FAILED FOR fd: %d [%s \n\n]", all_connections[i], strerror(errno));
                        break;
                    }
                }
                return_value--;
                if (!return_value) continue;
            }
        }
    }

    for( i = 0; i < Max_connect; i++){
        if(all_connections[i] > 0){
            close(all_connections[i]);
        }
    }
    return 0;
}
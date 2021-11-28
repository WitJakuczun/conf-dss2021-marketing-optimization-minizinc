%Parameters
int: pCustomersN;
int: pProductsN;
int: pChannelsN;
array[1..pCustomersN, 1..pProductsN, 1..pChannelsN] of float: pExpectedReve;
array[1..pChannelsN] of float: pChannelCosts;
float: pMaxBudget;
array[1..pProductsN] of int: pProductsMinOffersN;
float: pMinHurdleReve;

%Variables
array[1..pCustomersN, 1..pProductsN, 1..pChannelsN] of var 0..1: vAssignment;

%Constraints
constraint sum(customer in 1..pCustomersN, product in 1..pProductsN, channel in 1..pChannelsN)(vAssignment[customer, product, channel]*pChannelCosts[pChannelsN]) <= pMaxBudget;

constraint forall(product in 1..pProductsN) (
    sum(customer in 1..pCustomersN,
        channel in 1..pChannelsN) (
              vAssignment[customer, product, channel]
    ) >= pProductsMinOffersN[product]);

constraint sum(customer in 1..pCustomersN,
               product in 1..pProductsN,
               channel in 1..pChannelsN)
            (
                vAssignment[customer, product, channel]*pExpectedReve[customer, product, channel]
            ) >=
            (1+pMinHurdleReve)*sum(customer in 1..pCustomersN,
                                   product in 1..pProductsN,
                                   channel in 1..pChannelsN)
                                    (
                                        vAssignment[customer, product, channel]*pChannelCosts[pChannelsN]
                                    );

%product to customer only via max one channel
constraint forall(customer in 1..pCustomersN,
                  product in 1..pProductsN) (
    sum(channel in 1..pChannelsN)(
        vAssignment[customer, product, channel]
    ) <= 1
);

solve maximize sum(customer in 1..pCustomersN,
                   product in 1..pProductsN,
                   channel in 1..pChannelsN)
                (
                    vAssignment[customer, product, channel]*
                    pExpectedReve[customer, product, channel]
                );

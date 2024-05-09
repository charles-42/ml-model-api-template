      
az ad app create --display-name "Github_Login"

az ad app update --id c8e55b11-eab3-4556-a65c-3a95793dee90  --set groupMembershipClaims=All

az ad sp create --id c8e55b11-eab3-4556-a65c-3a95793dee90

az account set --subscription 111aaa69-41b9-4dfd-b6af-2ada039dd1ae

az role assignment create --assignee c8e55b11-eab3-4556-a65c-3a95793dee90 --role Contributor --scope subscriptions/111aaa69-41b9-4dfd-b6af-2ada039dd1ae

az ad sp credential reset --id c8e55b11-eab3-4556-a65c-3a95793dee90 --append --years 2
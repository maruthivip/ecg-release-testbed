import { gql, GraphQLClient } from "graphql-request";

const getOrder = gql`
  query GetOrder($id: ID!) {
    order(id: $id) { id }
  }
`;

export async function fetchOrder(client: GraphQLClient, id: string) {
  return client.request(getOrder, { id });
}

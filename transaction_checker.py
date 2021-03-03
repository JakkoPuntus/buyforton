from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


def check_transaction(transaction):
  # Select your transport with a defined url endpoint
  transport = AIOHTTPTransport(url="https://main.ton.dev/graphql")

  # Create a GraphQL client using the defined transport
  client = Client(transport=transport, fetch_schema_from_transport=True)

  # Provide a GraphQL query
  query = gql(
      """
  query{
    transactions(filter:{
      id:{
        eq:\"""" + transaction + """\"
      }
    })
    {
      status
      account_addr
      balance_delta
    }
  }
  """
  )

  # Execute the query on the transport
  result = client.execute(query)
  return result

print(check_transaction("dc3509d1bba15a30e71cefb237c068bdd64d0ea0578b1769c57a84a3dd7739c3"))
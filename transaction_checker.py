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
      out_msgs
    }
  }
  """
  )
  result = client.execute(query)
  return result



def check_message(message):
  # Select your transport with a defined url endpoint
  transport = AIOHTTPTransport(url="https://main.ton.dev/graphql")

  # Create a GraphQL client using the defined transport
  client = Client(transport=transport, fetch_schema_from_transport=True)

  query = gql(
    """
    query{messages( 
    filter: { 
      id:{eq:\"""" + str(message) +"""\"}
    }
    orderBy:{ path:"created_at", direction: DESC}
    limit: 1
  ) 
  { 
    dst
  } 
  }
    """
  )

  # Execute the query on the transport
  result = client.execute(query)
  return result
tr = check_transaction("f055324d031bcc5cf411e5ea5fb41900e3561c99a13403055fb594a18289e6d6")
a = tr["transactions"][0]["out_msgs"][0]
print(a)
print("s")
msg = check_message(a)
print(msg["messages"][0]["dst"])
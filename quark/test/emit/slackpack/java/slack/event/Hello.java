package slack.event;



/**
 * The client successfully connected to the server.
 */
public class Hello extends SlackEvent {
    public Hello() {
        super();
    }
    public void dispatch(slack.SlackHandler handler) {
        (handler).onHello(this);
    }
}
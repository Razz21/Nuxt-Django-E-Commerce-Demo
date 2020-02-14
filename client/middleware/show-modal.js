export default function({ store, route, redirect, from }) {
  /*
  auth-module does not allow to custom callback method for auth guard,
  this middleware use custom auth paths to open auth dialog
  */
  if (route.meta[0].modal) {
    if (!process.server) {
      /* show modal on client */
      store.commit("user/setDialog", route.name);
      /* stay on same page */
      return redirect(from);
    }
  }
  /* redirect to home page */
  redirect("/");
}

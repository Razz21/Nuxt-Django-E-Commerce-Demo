<template>
  <div class="h-full d-flex text-center justify-center align-center px-5">
    <div class="background">
      <ul class="circles">
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
      </ul>
    </div>
    <div class="notfound">
      <div class="notfound-code">
        <h3 class="headline text-uppercase">Oops! Page not found</h3>
        <h1><span>4</span><span>0</span><span>4</span></h1>
      </div>
      <h2 class="title text-uppercase">
        we are sorry, but the page you requested was not found
      </h2>
      <nuxt-link to="/">Back to home page</nuxt-link>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
@function randomNum($min, $max) {
  $rand: random();
  $randomNum: $min + floor($rand * (($max - $min) + 1));

  @return $randomNum;
}

.notfound {
  max-width: 520px;
  min-width: 300px;
  width: 100%;
  line-height: 1.4;
  margin: auto;
  color: #262626;

  &-code {
    h1 {
      line-height: 80%;
      font-size: 50vw;
      font-weight: 900;
      margin: 0px;
      text-transform: uppercase;
      letter-spacing: -30px;
      margin-left: -20px;
      @include breakpoint(sm) {
        font-size: 162px;
      }
      @include breakpoint(md) {
        font-size: 200px;
      }
      & > span {
        text-shadow: -8px 0px 0px #fff;
      }
    }
    h2 {
      margin-top: 0px;
      margin-bottom: 25px;
    }
    h3 {
      color: #262626;
      margin: 0px;
      letter-spacing: 3px;
    }
  }
}

.background {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, transparent 0%, #f5f3f1 70%);
  .circles {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    li {
      position: absolute;
      display: block;
      list-style: none;
      width: 20px;
      height: 20px;
      background: rgba(black, 0.07);
      animation: animate 25s linear infinite;
      bottom: -150px;
      @for $i from 1 through 10 {
        &:nth-child(#{$i}) {
          $size: #{randomNum(10, 120)}px;
          left: percentage(randomNum(10, 90) / 100);
          width: $size;
          height: $size;
          animation-delay: #{randomNum(0, 30)}s;
          animation-duration: #{randomNum(10, 30)}s;
        }
      }
    }
  }
}

@keyframes animate {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
    border-radius: 0;
  }

  100% {
    transform: translateY(-1000px) rotate(720deg);
    opacity: 0;
    border-radius: 50%;
  }
}
</style>

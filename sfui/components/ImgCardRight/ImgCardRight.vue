<template>
	<view class='Card'>
		<view>
			<uv-image width="345rpx"
			 :src='img_url' class="image" radius="8rpx 8rpx 0 0"></uv-image>
			<text class='tBox'>{{title}}</text>
		</view>
	</view>
</template>

<script>
	export default {
		name: "ImgCard",
		props:['img_url','title'],
		data() {
			return {

			};
		}
	}
</script>

<style lang="scss" scoped>
	.Card {
		width: 345rpx;
		height: auto;
		border-radius: 10rpx;
		margin-top: 10rpx;
		margin-bottom: 10rpx;
		margin-left: 10rpx;
		display: block;
		background-color:white;
		// border: solid 4rpx #FF5A5F;
		box-shadow:0 5rpx 5rpx rgba(0,0,0,0.1);
		.image{
			margin-bottom: 5rpx;
		}
		.tBox {
			color:#3E4C59;
			padding-left: 10rpx;
			padding-right: 10rpx;
			font-size: 30rpx;
		}
	}
</style>
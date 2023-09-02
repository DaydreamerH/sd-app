<template>
	<view class='CommentCard'>
		<view class='info'>
			<uv-avatar class='avatar' :src='comment.avatar' size="30"></uv-avatar>
			<view class='name_time'>
				<view class='name'>{{comment.uname}}</view>
				<view class='time'>{{comment.time}}</view>
			</view>
		</view>
		<view class='main'>
			<text class='text-wrap'>
				{{comment.text}}
			</text>
		</view>
		
		<uv-line length="700rpx" margin='25rpx'></uv-line>
	</view>
</template>

<script>
	export default {
		name: "Comment",
		props:['comment'],
		data() {
			return {

			};
		}
	}
</script>

<style lang="scss" scoped>
	.CommentCard {
		width: 750rpx;
		min-height: 200rpx;
		height: auto;
		margin-top: 20rpx;
		.info {
			width: auto;
			height: 100rpx;
			display: flex;
			
			.avatar {
				margin-left: 10rpx;
				margin-right: 10rpx;
				margin-top: 10rpx;
			}
			.name_time{
				min-width: 400rpx;
				width: auto;
				margin-left: 10rpx;
				height: auto;
				display: block;
				.name {
					margin-top: 10rpx;
					font-size: 30rpx;
					width: auto;
				}
				.time {
					margin-top: 5rpx;
					font-size: 20rpx;
				}
			}
		}
		.main{
			width: auto;
			margin-left: 90rpx;
			height: auto;
			min-height: 50rpx;
			font-size:38rpx;
			.text-wrap {
				word-break: break-all;
			}
		}
		.button_area{
			width: 750rpx;
			height:50rpx;
			display: flex;
			.chat_button{
				width: 80rpx;
				margin-left: 108rpx;
			}
		}
	}
</style>
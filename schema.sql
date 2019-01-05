/*
 Navicat Premium Data Transfer

 Source Server         : Aaron数据库
 Source Server Type    : PostgreSQL
 Source Server Version : 100006
 Source Host           : 112.74.32.21:5432
 Source Catalog        : ebooks
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 100006
 File Encoding         : 65001

 Date: 05/01/2019 15:33:51
*/


-- ----------------------------
-- Sequence structure for books_c_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."books_c_id_seq";
CREATE SEQUENCE "public"."books_c_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for muben_c_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."muben_c_id_seq";
CREATE SEQUENCE "public"."muben_c_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for books
-- ----------------------------
DROP TABLE IF EXISTS "public"."books";
CREATE TABLE "public"."books" (
  "id" int8 NOT NULL DEFAULT nextval('books_c_id_seq'::regclass),
  "title" varchar(1024) COLLATE "pg_catalog"."default",
  "contents" text COLLATE "pg_catalog"."default",
  "catalog" varchar(255) COLLATE "pg_catalog"."default",
  "author" varchar(64) COLLATE "pg_catalog"."default",
  "img_url" varchar(255) COLLATE "pg_catalog"."default",
  "pub_time" timestamp(6),
  "description" text COLLATE "pg_catalog"."default",
  "ISBN" varchar(255) COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."books"."id" IS '自增主键';
COMMENT ON COLUMN "public"."books"."title" IS '书籍标题';
COMMENT ON COLUMN "public"."books"."contents" IS '书籍目录';
COMMENT ON COLUMN "public"."books"."catalog" IS '书籍分类';
COMMENT ON COLUMN "public"."books"."author" IS '作者名称';
COMMENT ON COLUMN "public"."books"."img_url" IS '封面链接';
COMMENT ON COLUMN "public"."books"."pub_time" IS '发布时间';
COMMENT ON COLUMN "public"."books"."description" IS '书籍简介';
COMMENT ON COLUMN "public"."books"."ISBN" IS '唯一标号';

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "id" int8 NOT NULL DEFAULT nextval('muben_c_id_seq'::regclass),
  "username" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "password" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "p_email" varchar(255) COLLATE "pg_catalog"."default",
  "reg_phone" varchar(50) COLLATE "pg_catalog"."default",
  "reg_email" varchar(255) COLLATE "pg_catalog"."default",
  "reg_time" timestamp(6)
)
;
COMMENT ON COLUMN "public"."users"."username" IS '用户名';
COMMENT ON COLUMN "public"."users"."password" IS 'hash密码';
COMMENT ON COLUMN "public"."users"."p_email" IS '推送邮箱保存';
COMMENT ON COLUMN "public"."users"."reg_phone" IS '注册电话';
COMMENT ON COLUMN "public"."users"."reg_email" IS '注册邮箱';
COMMENT ON COLUMN "public"."users"."reg_time" IS '注册时间';

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."books_c_id_seq"', 2, false);
SELECT setval('"public"."muben_c_id_seq"', 2, false);

-- ----------------------------
-- Primary Key structure for table books
-- ----------------------------
ALTER TABLE "public"."books" ADD CONSTRAINT "ebooks_id" PRIMARY KEY ("id");
COMMENT ON CONSTRAINT "ebooks_id" ON "public"."books" IS '唯一键';

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");
